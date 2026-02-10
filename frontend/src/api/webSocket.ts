// src/api/websocket.ts
export function createSocket(): WebSocket {
  const token = localStorage.getItem("access_token");
  const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);
  ws.onopen = () => console.log("✅ WebSocket connected");
  ws.onclose = () => console.log("❌ WebSocket closed");
  ws.onerror = (e) => console.error("WebSocket error:", e);
  return ws;
}
