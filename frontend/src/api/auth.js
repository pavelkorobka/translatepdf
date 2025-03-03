import api from "./index"
import { setTokens } from "../utils/authHelper";;

export const login = () => {
  window.location.href = `${api.defaults.baseURL}/auth/google`;
};

export const refreshToken = async (refreshToken) => {
  const response = await api.post("/auth/refresh", { refresh_token: refreshToken });
  return response.data.access_token;
};

export const logout = async () => {
  await api.post("/auth/logout");
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  window.location.href = "/";
};