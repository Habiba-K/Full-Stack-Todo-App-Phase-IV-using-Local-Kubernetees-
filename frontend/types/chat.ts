/**
 * Chat-related TypeScript types for the AI chat agent feature.
 */

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  tool_calls: ToolCall[] | null;
  created_at: string;
}

export interface ToolCall {
  tool: string;
  input: Record<string, any>;
  result: Record<string, any>;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  message: ChatMessage;
}

export interface ChatHistoryResponse {
  conversation_id: string | null;
  messages: ChatMessage[];
  has_more: boolean;
}

export interface ChatHistoryParams {
  conversation_id?: string;
  limit?: number;
  before?: string;
}
