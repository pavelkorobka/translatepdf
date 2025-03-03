import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import Dashboard from "../views/Dashboard.vue";
import AuthCallback from "../views/AuthCallback.vue";

const routes = [
  { path: "/", component: LoginView },
  { path: "/dashboard", component: Dashboard },
  { path: "/auth/callback", component: AuthCallback },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;