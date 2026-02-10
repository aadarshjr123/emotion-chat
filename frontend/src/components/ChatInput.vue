<template>
  <div class="chat-input">
    <InputText
      v-model="textLocal"
      placeholder="Type a message..."
      class="input"
      @keyup.enter="sendMessage"
    />
    <Button
      icon="pi pi-send"
      label="Send"
      @click="sendMessage"
      class="send-btn"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import InputText from "primevue/inputtext";
import Button from "primevue/button";

const props = defineProps<{
  text: string;
  sendMessage: () => void;
}>();

const emit = defineEmits(["update:text"]);

const textLocal = ref(props.text);

watch(
  () => props.text,
  (newVal) => (textLocal.value = newVal)
);

watch(textLocal, (val) => emit("update:text", val));
</script>

<style scoped lang="scss">
.chat-input {
  display: flex;
  gap: 0.5rem;
  align-items: center;

  .input {
    flex: 1;
    padding: 0.6rem;
    border-radius: 8px;
  }

  .send-btn {
    border-radius: 8px;
    border: none;
  }
}
</style>
