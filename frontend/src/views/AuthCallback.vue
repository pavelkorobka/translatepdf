<script setup>
import { onMounted } from "vue";
import { useAuthStore } from "../store/authStore";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

onMounted(() => {
  try {
    const accessToken = route.query.access_token;
    const refreshToken = route.query.refresh_token;

    console.log("🔹 Полученный access_token:", accessToken);
    console.log("🔹 Полученный refresh_token:", refreshToken);
    alert("⚠️ Проверка токенов! Посмотри консоль.");

    if (!accessToken || !refreshToken) {
      console.error("❌ Ошибка: Токены отсутствуют в URL");
      setTimeout(() => router.push("/"), 3000); // Задержка перед редиректом
      return;
    }

    authStore.setAccessToken(accessToken);
    localStorage.setItem("refresh_token", refreshToken);

    console.log("✅ Токены успешно сохранены!");

    setTimeout(() => router.push("/dashboard"), 5000); // Задержка перед редиректом
  } catch (error) {
    alert("❌ Ошибка авторизации! Через 3 секунды редирект.");
    console.error("❌ Ошибка авторизации:", error);
    setTimeout(() => router.push("/"), 3000);
  }
});
</script>