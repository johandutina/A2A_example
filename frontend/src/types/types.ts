export interface ChatMessage {
  prompt: string;
  response?: {
    generatedCode: string;
    imageBase64: string;
    logs: string;
  };
  isLoading?: boolean;
  error?: string;
}

export interface ApiResponse {
  generated_code: string;
  image_base64: string;
  logs: string;
} 