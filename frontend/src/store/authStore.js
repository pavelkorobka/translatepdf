import { defineStore } from "pinia";
import { setTokens, clearTokens, refreshAccessToken } from "../utils/authHelper";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: localStorage.getItem("access_token") || null
  }),
  actions: {
    setAccessToken(token) {
      this.accessToken = token;
      setTokens(token, localStorage.getItem("refresh_token"));
    },
    async refreshAccessToken() {
      const newToken = await refreshAccessToken();
      if (newToken) this.setAccessToken(newToken);
    },
    logout() {
      clearTokens();
      this.accessToken = null;
      window.location.href = "/";
    }
  }
});