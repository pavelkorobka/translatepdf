import api from "../api";

export const getAccessToken = () => localStorage.getItem("access_token");
export const getRefreshToken = () => localStorage.getItem("refresh_token");

export const setTokens = (access, refresh) => {
  console.log("🔹 Сохраняем access_token:", access);
  console.log("🔹 Сохраняем refresh_token:", refresh);
  localStorage.setItem("access_token", access);
  localStorage.setItem("refresh_token", refresh);
};

export const clearTokens = () => {
  console.warn("⚠️ Токены очищены. Пользователь разлогинен.");
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

export const refreshAccessToken = async () => {
  try {
    const refreshToken = getRefreshToken();
    if (!refreshToken) {
      console.error("❌ Ошибка: Refresh token отсутствует.");
      throw new Error("Refresh token not found");
    }

    console.log("🔄 Обновляем access_token...");
    //const response = await api.post("/auth/refresh", { refresh_token: refreshToken });
    const response = await api.post(`/auth/refresh?refresh_token=${encodeURIComponent(refreshToken)}`);

    if (!response.data.access_token) {
      console.error("❌ Ошибка: Сервер не вернул новый access_token.");
      throw new Error("No access_token received");
    }

    setTokens(response.data.access_token, refreshToken);
    console.log("✅ Новый access_token успешно обновлён!");
    return response.data.access_token;
  } catch (error) {
    console.error("❌ Ошибка обновления access_token:", error.response?.data || error.message);
    
    // Если сервер вернул 403, значит refresh_token недействителен → разлогиниваем пользователя
    if (error.response?.status === 403) {
      console.warn("⚠️ Refresh token недействителен! Разлогиниваем пользователя.");
      clearTokens();
      alert("refresh");
      window.location.href = "/";
    }

    return null;
  }
};

// Автообновление токена при 401 ошибке
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      console.warn("⚠️ Получен 401. Пробуем обновить access_token...");
      const newToken = await refreshAccessToken();
      
      if (newToken) {
        console.log("🔁 Повторяем запрос с новым access_token.");
        error.config.headers.Authorization = `Bearer ${newToken}`;
        return api.request(error.config);
      }
    }
    
    return Promise.reject(error);
  }
);