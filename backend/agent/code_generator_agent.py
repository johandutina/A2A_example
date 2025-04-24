from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import matplotlib.pyplot as plt
import io
import base64
import contextlib
import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback
import numpy as np

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRequest(BaseModel):
    prompt: str

class AgentResponse(BaseModel):
    generated_code: str
    image_base64: str = ""
    logs: str

# Configure Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
    
genai.configure(api_key=api_key)

# === Real Agent Function using Gemini Flash 2 ===
def real_agent(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        response = model.generate_content([
            "You are a Python assistant that generates matplotlib code based on user prompts. "
            "Generate ONLY the raw Python code without any markdown formatting, backticks, or comments. "
            "The code should be valid Python that uses matplotlib to create visualizations. "
            "Include sample data if needed. Do not include ```python or ``` markers.",
            prompt
        ])
        
        # Clean the response by removing markdown code blocks
        code = response.text.strip()
        code = code.replace("```python", "").replace("```", "").strip()
        
        print("Generated code after cleaning:", code)  # Debug print
        return code
    except Exception as e:
        return f"# Error generating code: {str(e)}"

# === Code Execution + Chart Capture ===
def run_code_and_capture_image(code: str):
    stdout_capture = io.StringIO()
    image_data = ""
    try:
        # Create a new figure before executing the code
        plt.figure()
        
        with contextlib.redirect_stdout(stdout_capture):
            # Create a safe globals dictionary with only matplotlib
            exec_globals = {
                "plt": plt,
                "numpy": np,  # Add numpy if needed
                "np": np     # Common numpy alias
            }
            
            # Execute the code
            exec(code, exec_globals)
            
            # Save the figure to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            # Close the figure to free memory
            plt.close()
            
        return {
            "logs": stdout_capture.getvalue() or "Code executed successfully",
            "image_base64": image_data
        }
    except Exception as e:
        error_msg = f"Error executing code: {str(e)}\n{traceback.format_exc()}"
        return {
            "logs": error_msg,
            "image_base64": ""
        }

# === API Endpoint ===
@app.post("/agent/code", response_model=AgentResponse)
async def generate_code_and_image(request: AgentRequest):
    try:
        # Generate code using Gemini
        code = real_agent(request.prompt)
        
        # Log the generated code for debugging
        print("Generated code:", code)
        
        # Execute the code and capture results
        result = run_code_and_capture_image(code)
        
        return AgentResponse(
            generated_code=code,
            logs=result["logs"],
            image_base64=result["image_base64"]
        )
    except Exception as e:
        error_msg = f"Error in generate_code_and_image: {str(e)}\n{traceback.format_exc()}"
        return AgentResponse(
            generated_code="# Error occurred",
            logs=error_msg,
            image_base64=""
        )

# === A2A Agent Metadata Endpoint ===
@app.get("/agent/code_generator_agent/metadata")
def get_agent_metadata():
    return {
        "agent_id": "code_visualizer_agent",
        "version": "1.0.0",
        "description": "An AI agent that takes natural language prompts, generates Python matplotlib code using Gemini Flash 2, executes the code, and returns a visual plot and execution logs.",
        "modality": ["text", "code", "image"],
        "inputs": {
            "type": "text",
            "format": "natural language prompt"
        },
        "outputs": {
            "generated_code": "Python code (string)",
            "image_base64": "Base64-encoded PNG image",
            "logs": "Standard output or error logs"
        },
        "skills": [
            "code_generation",
            "data_visualization",
            "code_execution",
            "gemini_integration"
        ],
        "tools": [
            {
                "name": "Gemini Flash 2",
                "type": "language_model",
                "provider": "Google",
                "model": "gemini-1.5-flash-latest"
            },
            {
                "name": "Matplotlib",
                "type": "visualization_library",
                "language": "Python"
            }
        ],
        "interface": {
            "type": "REST",
            "endpoint": "/agent/code",
            "method": "POST",
            "request_format": {
                "prompt": "string"
            },
            "response_format": {
                "generated_code": "string",
                "image_base64": "string",
                "logs": "string"
            }
        },
        "invocation": {
            "type": "synchronous",
            "execution_environment": "FastAPI (Python)",
            "security": "API key required for Gemini access"
        }
    }
