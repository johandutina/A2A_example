import React, { useState } from 'react';
import { generateCode } from '../services/api';

export const Chat: React.FC = () => {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState<{
    code?: string;
    image?: string;
    logs?: string;
    error?: string;
  }>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsLoading(true);
    setResponse({});

    try {
      const result = await generateCode(input);
      setResponse({
        code: result.generated_code,
        image: result.image_base64,
        logs: result.logs
      });
    } catch (error) {
      setResponse({ error: 'Failed to generate response' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Input Form */}
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe the visualization you want (e.g., 'Create a bar chart showing monthly sales')"
            className="flex-1 p-3 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
          >
            {isLoading ? 'Generating...' : 'Generate'}
          </button>
        </div>
      </form>

      {/* Response Display */}
      <div className="space-y-6">
        {isLoading && (
          <div className="text-center text-gray-600">
            Generating visualization...
          </div>
        )}

        {response.error && (
          <div className="p-4 bg-red-100 text-red-700 rounded-lg">
            {response.error}
          </div>
        )}

        {response.code && (
          <div className="bg-gray-100 rounded-lg p-4">
            <h3 className="font-medium mb-2">Generated Code:</h3>
            <pre className="bg-gray-800 text-white p-4 rounded overflow-x-auto">
              {response.code}
            </pre>
          </div>
        )}

        {response.image && (
          <div className="bg-white rounded-lg p-4 shadow">
            <h3 className="font-medium mb-2">Generated Visualization:</h3>
            <img
              src={`data:image/png;base64,${response.image}`}
              alt="Generated visualization"
              className="max-w-full h-auto rounded"
            />
          </div>
        )}

        {response.logs && (
          <div className="bg-gray-100 rounded-lg p-4">
            <h3 className="font-medium mb-2">Execution Logs:</h3>
            <pre className="bg-gray-800 text-white p-4 rounded overflow-x-auto">
              {response.logs}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat; 