<template>
  <div class="chat-message" :class="isMine ? 'mine' : 'other'">
    <div class="bubble">
      <div class="meta">
        <span class="user">{{ isMine ? "You" : message.sender_name || "User " + message.sender_id }}</span>
        <span class="emoji">{{ emoji(message.emotion) }}</span>
      </div>
      <p class="text">{{ message.text }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { ChatMessage } from "../types/chat";
import { useAuth } from "../composables/useAuth";

const props = defineProps<{ message: ChatMessage }>();
const { userId } = useAuth();

const isMine = computed(() => props.message.sender_id === userId.value);

const emoji = (emotion: string): string => {
  if (emotion === "positive") return "😄";
  if (emotion === "negative") return "😞";
  return "😐";
};
</script>

<style scoped lang="scss">
.chat-message {
  display: flex;
  margin: 0.5rem 0;
  font-size: 0.95rem;
  transition: all 0.2s ease-in-out;

  &.mine {
    justify-content: flex-end;

    .bubble {
      background: var(--primary-color);
      color: black;
      border-top-right-radius: 0;
    }
  }

  &.other {
    justify-content: flex-start;

    .bubble {
      background: var(--surface-section);
      color: var(--text-color);
      border-top-left-radius: 0;
    }
  }

  .bubble {
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    max-width: 70%;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }

  .meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    margin-bottom: 0.25rem;
    opacity: 0.85;
  }

  .emoji {
    font-size: 1.1rem;
  }

  .text {
    word-wrap: break-word;
    line-height: 1.4;
  }
}
</style>
