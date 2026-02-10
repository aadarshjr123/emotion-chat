import { createRouter, createWebHistory } from "vue-router";
import ChatView from "../views/ChatView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import HomeView from "../views/HomeView.vue";
import ProfileSettings from "../views/ProfileSettings.vue"; // <-- import it directly
// <-- import it directly

const routes = [
  { path: "/", redirect: "/home" },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { guestOnly: true },
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
    meta: { guestOnly: true },
  },
  {
    path: "/home",
    name: "home",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/chat/:id",
    name: "chat",
    component: ChatView,
    meta: { requiresAuth: true },
    props: true, // ✅ pass id as prop to ChatView
  },
  {
    path: "/profile",
    name: "profile",
    component: ProfileSettings,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, _, next) => {
  const token = localStorage.getItem("access_token");

  // Auth protection
  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;
