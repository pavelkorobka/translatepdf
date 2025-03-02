import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import Dashboard from "../views/Dashboard.vue";

const routes = [
  { path: "/", component: LoginView },
  { path: "/dashboard", component: Dashboard }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;