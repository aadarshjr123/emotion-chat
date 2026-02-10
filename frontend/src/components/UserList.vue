<template>
  <div class="user-list">
    <h3 class="title">Online Users</h3>

    <div v-if="users.length" class="list">
      <div
        v-for="u in users"
        :key="u.id"
        class="item"
        :class="{ active: u.id === selectedUser }"
        @click="$emit('select', u.id)"
      >
        <i class="pi pi-user"></i>
        <span>{{ u.username || "User " + u.id }}</span>
      </div>
    </div>

    <Message
      v-else
      severity="info"
      class="info-msg"
      :closable="false"
    >
      No users online.
    </Message>
  </div>
</template>

<script setup lang="ts">
import Message from "primevue/message";

defineProps<{
  users: { id: number; username: string }[];
  selectedUser: number | null;
}>();

defineEmits(["select"]);
</script>

<style scoped lang="scss">
.user-list {
  background: var(--surface-card);
  padding: 1rem;
  border-right: 1px solid var(--surface-border);
  height: 100%;
  overflow-y: auto;
  border-radius: 10px 0 0 10px;

  .title {
    margin-bottom: 1rem;
    font-weight: 600;
    color: var(--text-color);
  }

  .list {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 0.8rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s ease;

    &:hover {
      background: var(--surface-hover);
    }

    &.active {
      background: var(--primary-color);
      color: white;

      i {
        color: white;
      }
    }

    i {
      color: var(--primary-color);
    }
  }

  .info-msg {
    font-size: 0.85rem;
  }
}
</style>
