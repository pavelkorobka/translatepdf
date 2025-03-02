import api from "./index";

export const getCurrentUser = async () => api.get("/users/me");

export const getAllUsers = async () => api.get("/users/");

export const deleteUser = async () => api.delete("/users/me");