# Importing required Python libraries and tools
# These handle web requests, security, data validation, chart creation, AI integration, and environment settings
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

# Load secret keys and configuration from a .env file (e.g., the Gemini API key)
load_dotenv()

# Create the web application using FastAPI
app = FastAPI()

# Enable access from other websites or applications (CORS settings)
# This is useful if you are using this API from a different frontend (like a web app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any website; in production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what kind of input the API expects: a prompt from the user
class AgentRequest(BaseModel):
    prompt: str

# Define what kind of response the API will return:
# 1. Generated Python code
# 2. A visual image as a base64 string
# 3. Any logs or messages from the code execution
class AgentResponse(BaseModel):
    generated_code: str
    image_base64: str = ""
    logs: str

# Read the API key needed to talk to Google's Gemini AI from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Initialize the Gemini AI using the API key
genai.configure(api_key=api_key)

# === AI Agent Function: Talks to Google's Gemini AI ===
# This function sends the user's prompt to the AI and asks it to generate Python code that creates a chart
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
        
        # Clean up the result by removing unwanted formatting
        code = response.text.strip()
        code = code.replace("```python", "").replace("```", "").strip()

        print("Generated code after cleaning:", code)  # For developers: see what the AI returned
        return code
    except Exception as e:
        # If something goes wrong, return an error message in code format
        return f"# Error generating code: {str(e)}"

# === Code Execution and Image Capture ===
# This function runs the generated code and captures any visual chart it creates
def run_code_and_capture_image(code: str):
    stdout_capture = io.StringIO()  # This collects any print statements or logs
    image_data = ""
    try:
        plt.figure()  # Prepare to draw a new chart
        
        with contextlib.redirect_stdout(stdout_capture):
            # Set up a safe environment for running the code with only certain libraries allowed
            exec_globals = {
                "plt": plt,
                "numpy": np,
                "np": np
            }

            # Run the Python code (from the AI) inside this safe environment
            exec(code, exec_globals)

            # Save the resulting chart to memory (not to a file)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')  # Save as PNG
            buf.seek(0)
            image_data = base64.b64encode(buf.getvalue()).decode('utf-8')  # Convert image to base64 for web delivery

            plt.close()  # Clean up the memory used for plotting

        return {
            "logs": stdout_capture.getvalue() or "Code executed successfully",
            "image_base64": image_data
        }
    except Exception as e:
        # If there’s an error, return the error message and no image
        error_msg = f"Error executing code: {str(e)}\n{traceback.format_exc()}"
        return {
            "logs": error_msg,
            "image_base64": ""
        }

# === Main API Endpoint ===
# This is the main function that runs when someone sends a prompt to the API
@app.post("/agent/code", response_model=AgentResponse)
async def generate_code_and_image(request: AgentRequest):
    try:
        # Step 1: Ask Gemini AI to generate code based on the user’s prompt
        code = real_agent(request.prompt)

        # Step 2: Show the generated code in the server logs (for developers)
        print("Generated code:", code)

        # Step 3: Run the code and get the result (chart image + logs)
        result = run_code_and_capture_image(code)

        # Step 4: Return everything to the user
        return AgentResponse(
            generated_code=code,
            logs=result["logs"],
            image_base64=result["image_base64"]
        )
    except Exception as e:
        # If something breaks during the process, return an error in the response
        error_msg = f"Error in generate_code_and_image: {str(e)}\n{traceback.format_exc()}"
        return AgentResponse(
            generated_code="# Error occurred",
            logs=error_msg,
            image_base64=""
        )

# === Metadata Endpoint ===
# This returns information about the AI agent for documentation or discovery purposes
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
