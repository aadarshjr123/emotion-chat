<template>
  <div class="chat-container">
    <div class="chat-card">
      <header class="chat-header">
        <div class="chat-header-info">
          <i class="pi pi-comments chat-icon"></i>
          <h2 v-if="selectedUserName">
            Chat with <span class="chat-user">{{ selectedUserName }}</span>
          </h2>
          <h2 v-else>Select a user to start chatting</h2>
        </div>
        <Button
          label="Back"
          icon="pi pi-arrow-left"
          severity="secondary"
          size="small"
          @click="goBack"
        />
      </header>

      
      <ScrollPanel class="chat-messages" ref="chatBox">
        <ChatMessage v-for="(msg, i) in messages" :key="i" :message="msg" />
      </ScrollPanel>
      <footer class="chat-footer">
        <ChatInput v-model:text="text" :send-message="sendMessage" />
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useChat } from "../composables/useChat";
import { useAutoScroll } from "../composables/useAutoScroll";
import { getHistory } from "../api/messages";

// ✅ PrimeVue components
import Button from "primevue/button";
import ScrollPanel from "primevue/scrollpanel";

// ✅ Chat components
import ChatMessage from "../components/ChatMessage.vue";
import ChatInput from "../components/ChatInput.vue";

const route = useRoute();
const router = useRouter();
const { selectedUser, messages, text, connect, sendMessage } = useChat();
const chatBox = ref<HTMLDivElement | null>(null);

onUnmounted(() => {
  selectedUser.value = null; // 🧹 ensures notifications work on Home page
});

useAutoScroll(chatBox, messages);

const selectedUserName = computed(() => localStorage.getItem("last_chat_username"));

onMounted(async () => {
  connect();

  const otherUserId = Number(route.params.id);
  if (otherUserId) {
    selectedUser.value = otherUserId;
    messages.value = await getHistory(otherUserId);
    localStorage.setItem("last_chat_user", String(otherUserId));
  }
});

watch(
  () => route.params.id,
  async (newId) => {
    if (newId) {
      selectedUser.value = Number(newId);
      messages.value = await getHistory(Number(newId));
      localStorage.setItem("last_chat_user", String(newId));
    }
  }
);

function goBack() {
  router.push("/home");
}
</script>

<style scoped lang="scss">
.chat-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  background-color: var(--surface-ground);
  padding: 1.5rem;
}

.chat-card {
  background: var(--surface-card);
  border-radius: 10px;
  width: 100%;
  max-width: 700px;
  height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.2rem;
  background: var(--surface-section);
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  
  h2 {
    font-size: 1.2rem;
    color: var(--text-color);
    font-weight: 600;
  }
  
  .chat-user {
    color: var(--primary-color);
  }
  
  .chat-icon {
    color: var(--primary-color);
    font-size: 1.5rem;
    margin-right: 0.5rem;
  }
}

.chat-messages {
  display: flex;
  flex: 1;
  padding: 1rem;
  overflow: hidden;
  background-color: var(--surface-section);
}

.chat-footer {
  // border-style: dashed;
  padding: 1rem;
  background: var(--surface-section);
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}
</style>
