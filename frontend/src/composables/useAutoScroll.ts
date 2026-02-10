import { watch, type Ref, nextTick } from "vue";
import type { ChatMessage } from "../types/chat";

export function useAutoScroll(
  container: Ref<HTMLElement | null>,
  messages: Ref<ChatMessage[]>
) {
  watch(messages, async () => {
    await nextTick();
    if (container.value) {
      container.value.scrollTop = container.value.scrollHeight;
    }
  });
}
