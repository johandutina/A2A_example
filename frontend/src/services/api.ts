import { ApiResponse } from '../types/types';

const API_BASE_URL = 'http://localhost:8000';

export const generateCode = async (prompt: string): Promise<ApiResponse> => {
  const response = await fetch(`${API_BASE_URL}/agent/code`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error('Failed to generate code');
  }

  return response.json();
}; 