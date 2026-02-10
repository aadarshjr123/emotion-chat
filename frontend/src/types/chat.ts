export interface ChatMessage {
  sender_id: number;
  receiver_id: number;
  text: string;
  emotion: string;
  sender_name?: string; // optional for display
}
