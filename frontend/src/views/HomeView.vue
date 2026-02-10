<template>
  <div class="home-container">
    <div class="home-card">
      <div class="profile-summary__header">
        <div class="profile-summary__info">
          <!-- ✅ Prevent broken image: only render image avatar if url exists -->
          <Avatar
            v-if="profileImage"
            class="profile-summary__avatar"
            :image="profileImage"
            shape="circle"
          />
          <Avatar
            v-else
            class="profile-summary__avatar"
            icon="pi pi-user"
            shape="circle"
          />

          <strong>{{ username }}</strong>
        </div>

        <div class="profile-summary__chart">
          <h3 class="section-title">Your Emotion Summary</h3>
          <Chart type="pie" :data="chartData" :options="chartOptions" />
        </div>
      </div>

      <!-- 🔹 Search -->
      <section class="home-section">
        <h3 class="section-title">Search Users</h3>

        <div class="search-box">
          <InputText
            v-model="query"
            placeholder="Search by username..."
            class="search-input"
          />
          <Button
            icon="pi pi-search"
            class="search-btn"
            @click="fetchUsers(query)"
          />
        </div>

        <div
          v-for="u in results"
          :key="u.id"
          class="search-user-item"
          @click="openChat(u.id)"
        >
          <Avatar
            v-if="u.profile_picture"
            :image="toMediaUrl(u.profile_picture)"
            class="avatar-search"
            shape="circle"
          />
          <Avatar
            v-else
            icon="pi pi-user"
            shape="circle"
            class="avatar-search"
            style="background-color: #e0e0e0"
          />
          <span class="avatar-name">{{ u.username }}</span>
        </div>
      </section>

      <!-- 🔹 Recent Chats -->
      <section class="home-section">
        <h3 class="section-title">Recently Talked Users</h3>

        <div v-if="recent.length" class="user-list">
          <div
            v-for="u in recent"
            :key="u.id"
            class="user-item"
            @click="openChat(u.id)"
          >
            <Avatar
              v-if="u.profile_picture"
              :image="toMediaUrl(u.profile_picture)"
              class="avatar-search"
              shape="circle"
            />
            <Avatar
              v-else
              icon="pi pi-user"
              shape="circle"
              class="avatar-search"
              style="background-color: #e0e0e0"
            />

            <div>
              <strong>{{ u.username }}</strong>
              <p class="last-message">{{ u.lastMessage }}</p>
            </div>
          </div>
        </div>

        <Message v-else severity="info" class="info-msg" :closable="false">
          No recent chats yet.
        </Message>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import debounce from "lodash.debounce";

// ✅ APIs
import { searchUsers, getRecentUsers, fetchEmotionStats } from "../api/users";

// ✅ State
import { useAuth } from "../composables/useAuth";
import { useChat } from "../composables/useChat";

// ✅ Utils
import { toMediaUrl } from "../utils/media";

// ✅ PrimeVue
import Avatar from "primevue/avatar";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Message from "primevue/message";
import Chart from "primevue/chart";

const router = useRouter();

// ✅ Use reactive auth state (NOT localStorage)
const auth = useAuth();
const username = computed(() => auth.username.value || "");
const token = computed(() => auth.token.value);
const profileImage = computed(() => toMediaUrl(auth.profilePicture.value));

// ✅ Chat shared state
const { connect, recent } = useChat();

// 🔹 Search
const query = ref("");
const results = ref<any[]>([]);

// 🔹 Emotion stats + chart
const emotionStats = ref({ happy: 0, sad: 0 });

const chartData = ref({
  labels: ["Happy 😀", "Sad 😢"],
  datasets: [
    {
      data: [0, 0],
      backgroundColor: ["#66BB6A", "#EF5350"],
      hoverBackgroundColor: ["#81C784", "#E57373"],
    },
  ],
});

const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: {
      position: "bottom",
      labels: { color: "#495057" },
    },
  },
});

onMounted(async () => {
  // ✅ ensure websocket connection (for realtime updates)
  if (token.value) connect();

  // ✅ preload recent from backend (for persistence)
  if (!recent.value.length) {
    try {
      const res = await getRecentUsers();
      recent.value = Array.isArray(res)
        ? res.map((u: any) => ({ ...u, lastMessage: "" }))
        : [];
    } catch (err) {
      console.error("Failed to load recent users:", err);
    }
  }

  // ✅ load emotion stats
  try {
    const res = await fetchEmotionStats();
    emotionStats.value = res;
    chartData.value.datasets[0].data = [res.happy, res.sad];
  } catch (err) {
    console.error("Failed to load emotion stats:", err);
  }
});

const fetchUsers = debounce(async (q: string) => {
  if (!q.trim()) {
    results.value = [];
    return;
  }
  try {
    const res = await searchUsers(q);
    results.value = Array.isArray(res) ? res : [];
  } catch (err) {
    console.error("Search failed:", err);
    results.value = [];
  }
}, 400);

watch(query, fetchUsers);

function openChat(id: number) {
  const user = [...recent.value, ...results.value].find((u) => u.id === id);
  if (!user) return;

  localStorage.setItem("last_chat_user", String(user.id));
  localStorage.setItem("last_chat_username", user.username);

  router.push({ name: "chat", params: { id: user.id } });
}
</script>

<style scoped lang="scss">
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: var(--surface-ground);
  min-height: 100vh;
}

.profile-summary__header {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  gap: 2rem;
  width: 50rem;
}

.profile-summary__info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-summary__chart {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.p-avatar-circle {
  width: 20rem;
  height: 20rem;
  overflow: hidden;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* make sure the actual <img> inside Avatar is styled correctly */
:deep(.p-avatar img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.last-message {
  font-size: 0.85rem;
  color: #666;
  margin: 0;
  margin-top: 2px;
  max-width: 240px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.home-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--surface-card);
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 2rem;
  width: 100%;
  max-width: 800px;
}

.home-section {
  display: flex;
  flex-direction: column;
  margin-bottom: 2rem;
  width: 100%;
}

.section-title {
  margin-bottom: 1rem;
  color: var(--text-color);
  font-weight: 600;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.search-user-item {
  height: 3rem;
  display: flex;
  justify-items: center;
  align-items: center;
  gap: 0.5rem;

  .avatar-search {
    display: flex;
    height: 2rem;
    width: 2rem;
  }

  .avatar-name {
    display: flex;
    font-weight: 500;
  }
}

.user-item {
  height: 2rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.7rem 1rem;
  background: var(--surface-section);
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;

  .avatar-search {
    display: flex;
    height: 2rem;
    width: 2rem;
  }

  &:hover {
    background: var(--surface-hover);
  }
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;

  .search-input {
    flex: 1;
  }
}

.search-btn {
  flex-shrink: 0;
}

.p-message {
  border: none;
  outline-style: none;
}

.info-msg {
  font-size: 0.9rem;
  background-color: var(--surface-section);
  color: black;
}
</style>