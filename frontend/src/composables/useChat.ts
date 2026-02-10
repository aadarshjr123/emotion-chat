// src/composables/useChat.ts
import { ref, onUnmounted } from "vue";
import { useAuth } from "./useAuth";
import { getHistory } from "../api/messages";
import { useRoute } from "vue-router";

const users = ref<{ id: number; username: string }[]>([]);
const selectedUser = ref<number | null>(null);
const messages = ref<any[]>([]);
const notifications = ref<any[]>([]);
const text = ref("");
const messageQueue: any[] = [];
const recent = ref<
  {
    id: number;
    username: string;
    lastMessage: string;
    profile_picture: string;
  }[]
>([]);

let ws: WebSocket | null = null;
let isConnected = false;
let reconnectTimer: any = null;

export function useChat() {
  const { token, userId } = useAuth();
  const route = useRoute();

  function connect() {
    // ✅ Already connected or connecting
    if (isConnected || ws || !token.value) return;

    ws = new WebSocket(`ws://localhost:8000/ws?token=${token.value}`);

    ws.onopen = () => {
      console.log("✅ WebSocket connected");
      isConnected = true;
      clearTimeout(reconnectTimer);

      // 🔁 Send any messages queued while disconnected
      flushQueue();

      // 📌 Restore last selected chat (optional)
      const lastChat = localStorage.getItem("last_chat_user");
      if (lastChat) {
        selectedUser.value = Number(lastChat);
      }
    };

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);

      if (msg.type === "users") {
        users.value = msg.users.filter((u: any) => u.id !== userId.value);
        return;
      }

      if (msg.type === "message") {
        const me = userId.value;
        const partner = selectedUser.value;

        // Are we currently inside this exact conversation?
        const inThisChat =
          partner !== null &&
          ((msg.sender_id === partner && msg.receiver_id === me) ||
            (msg.sender_id === me && msg.receiver_id === partner));

        if (inThisChat) {
          messages.value.push(msg);
          return;
        }

        // If I'm receiving a message and I'm NOT in that chat -> notification
        if (msg.receiver_id === me) {
          notifications.value.unshift({
            sender_id: msg.sender_id,
            sender_name: msg.sender_name || `User ${msg.sender_id}`,
            text: msg.text,
            emotion: msg.emotion,
            timestamp: new Date().toISOString(),
          });
          playNotificationSound();
        }

        return;
      }

      if (msg.type === "notification") {
        notifications.value.unshift(msg);
        playNotificationSound();
        return;
      }
    };

    ws.onclose = () => {
      console.warn("❌ WebSocket closed. Attempting reconnect...");
      isConnected = false;
      ws = null;

      if (token.value) {
        reconnectTimer = setTimeout(connect, 3000); // 🔁 Retry in 3s
      }
    };

    ws.onerror = (err) => {
      console.error("❌ WebSocket error:", err);
      ws?.close(); // This will trigger `onclose` logic
    };
  }

  const sendQueue: string[] = [];
  function flushQueue() {
    if (ws && ws.readyState === WebSocket.OPEN) {
      while (sendQueue.length > 0) {
        const msg = sendQueue.shift();
        if (msg) ws.send(msg);
      }
    }
  }

  function sendMessage() {
    if (!text.value.trim() || !selectedUser.value) return;

    const payload = {
      text: text.value.trim(),
      receiver_id: selectedUser.value,
    };

    const messageString = JSON.stringify(payload);

    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(messageString);
    } else {
      console.warn("⚠️ Socket not ready, queuing message.");
      sendQueue.push(messageString);
    }

    text.value = "";
  }

  async function selectUser(id: number) {
    selectedUser.value = id;
    localStorage.setItem("last_chat_user", String(id));
    messages.value = await getHistory(id);
    notifications.value = notifications.value.filter((n) => n.sender_id !== id);
  }

  function disconnect() {
    clearTimeout(reconnectTimer);
    if (ws) ws.close();
    ws = null;
    isConnected = false;
  }

  function playNotificationSound() {
    const audio = new Audio("/sounds/notification.wav");
    audio.volume = 0.4;
    audio.play().catch(() => {});
  }

  return {
    users,
    recent,
    selectedUser,
    messages,
    notifications,
    text,
    connect,
    disconnect,
    selectUser,
    sendMessage,
  };
}
