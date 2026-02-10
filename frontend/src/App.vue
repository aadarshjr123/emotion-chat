<template>
  <div id="app">
    <AppHeader v-if="isLoggedIn" />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import AppHeader from "./components/AppHeader.vue";
import { computed, watch } from "vue";
import { useAuth } from "./composables/useAuth";
import { useChat } from "./composables/useChat";
import { useRoute } from "vue-router";
const { token } = useAuth();
const isLoggedIn = computed(() => !!token.value);
const route = useRoute();


const { connect } = useChat();

watch(
  () => route.path,
  () => {
    if (token.value) {
      connect(); // reconnect on route change if token exists
    }
  },
  { immediate: true }
);
</script>


<style>
html, body, #app {
  height: 100%;
  margin: 0;
  font-family: system-ui, sans-serif;
  background-color: #f7f9fb;
}
</style>
