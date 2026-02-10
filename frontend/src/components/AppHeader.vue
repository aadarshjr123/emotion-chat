<template>
  <header class="app-header">
    <h1 class="app-header__logo">💬 EmotiChat</h1>

    <div class="header-actions">
      <!-- 🔔 Notifications -->

      {{ console.log(notifications.length) }}
      <OverlayBadge size="small" severity="contrast" :value="String(notifications.length)">
        <Button
        icon="pi pi-bell"
        class="p-button-rounded p-button-text"
        @click="toggleNotifPanel"
        />
      </OverlayBadge>
      <OverlayPanel ref="notifPanel" style="width: 250px">
        <template v-if="notifications.length">
          <div class="notif-list">
            <div
              v-for="(n, i) in notifications"
              :key="i"
              class="notif-item"
              @click="openChat(n.sender_id, n.sender_name)"
            >
              <strong>{{ n.sender_name }}</strong>
              <p>{{ n.text }}</p>
            </div>
            <Button
              label="Clear All"
              icon="pi pi-trash"
              class="p-button-sm p-button-text"
              severity="danger"
              @click="clearAllNotifications"
            />
          </div>
        </template>
        <template v-else>
          <p class="empty">No new notifications</p>
        </template>
      </OverlayPanel>

      <!-- 🏠 Home -->
      <Button
        icon="pi pi-home"
        class="p-button-rounded p-button-text"
        @click="goHome"
        
      />

      <!-- 👤 Profile dropdown -->
      <div class="profile-menu">
        <Avatar
          :image="profilePicUrl"
          shape="circle"
          class="profile-avatar"
          @click="toggleProfilePanel"
        />
        <OverlayPanel ref="profilePanel" style="width: 160px">
          <div class="profile-dropdown">
            <div class="profile-info">
              <strong>{{ username }}</strong>
            </div>
            <Button
              label="Profile"
              icon="pi pi-cog"
              class="p-button-text"
              @click="goToProfile"
            />
            <Button
              label="Logout"
              icon="pi pi-sign-out"
              class="p-button-text p-button-danger"
              @click="logout"
            />
          </div>
        </OverlayPanel>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";
import { useChat } from "../composables/useChat";

import Button from "primevue/button";
import OverlayPanel from "primevue/overlaypanel";
import OverlayBadge from "primevue/overlaybadge";

import Avatar from "primevue/avatar";

const { username, logout } = useAuth();
const { notifications } = useChat();
const router = useRouter();

// const profilePic = localStorage.getItem("profile_picture");
// const profilePicUrl = profilePic ? `http://localhost:8000${profilePic}` : "";

const notifPanel = ref();
const profilePanel = ref();
const profilePic = ref(localStorage.getItem("profile_picture") || "");

const profilePicUrl = computed(() =>
  profilePic.value ? `http://localhost:8000${profilePic.value}` : ""
);

onMounted(() => {
  profilePic.value = localStorage.getItem("profile_picture") || "";

  // ✅ Listen for profile picture updates from ProfileSettings.vue
  window.addEventListener("profile-updated", (e: any) => {
    profilePic.value = e.detail;
  });
});

onUnmounted(() => {
  window.removeEventListener("profile-updated", () => {});
});

function toggleNotifPanel(event: Event) {
  profilePanel.value?.hide();
  notifPanel.value.toggle(event);
}

function toggleProfilePanel(event: Event) {
  notifPanel.value?.hide();
  profilePanel.value.toggle(event);
}

function clearAllNotifications() {
  notifications.value = [];
}

function goToProfile() {
  profilePanel.value?.hide();
  router.push("/profile");
}

function goHome() {
  router.push("/home");
}

function openChat(id: number, name: string) {
  localStorage.setItem("last_chat_user", String(id));
  localStorage.setItem("last_chat_username", name);

  notifications.value = notifications.value.filter(n => n.sender_id !== id);
  notifPanel.value?.hide();
  router.push({ name: "chat", params: { id } });
}
</script>

<style scoped lang="scss">
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(90deg, #66ea87, #4ba28f);
  color: white;
  padding: 0.75rem 1.5rem;
  position: sticky;
  top: 0;
  z-index: 1000;

  &__logo {
    font-size: 1.4rem;
    font-weight: bold;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 0.8rem;
  }

  .profile-menu {
    position: relative;
    cursor: pointer;

    .profile-avatar {
      width: 32px;
      height: 32px;
      border: 2px solid white;
    }

    .profile-dropdown {
      display: flex;
      flex-direction: column;
      gap: 0.4rem;

      .p-button-text {
        justify-content: flex-start;
        padding: 0.3rem 0.6rem;
      }
    }
  }

  .p-button-text {
    color: white
  }

  .notif-list {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;

    .notif-item {
      padding: 0.5rem;
      border-bottom: 1px solid #eee;
      cursor: pointer;

      strong {
        display: block;
      }

      p {
        margin: 0;
        font-size: 0.85rem;
      }

      &:hover {
        background-color: #f9f9f9;
      }
    }

    .p-button-danger {
      align-self: flex-end;
      margin-top: 0.5rem;
    }
  }

  .empty {
    text-align: center;
    color: #888;
    font-size: 0.9rem;
    padding: 1rem 0;
  }
}
</style>
