<template>
  <div>
    <h2>Ваши файлы</h2>
    <input type="file" @change="handleFileUpload" />
    <ul>
      <li v-for="file in files" :key="file">{{ file }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { uploadFile, getFiles } from "../api/files";
import { useAuthStore } from "../store/authStore"; // Добавили импорт состояния авторизации

const files = ref([]);
const authStore = useAuthStore(); // Получаем доступ к хранилищу токенов

const loadFiles = async () => {
  console.log("⏳ Проверяем авторизацию перед загрузкой файлов...");

  // Загружаем файлы ТОЛЬКО если access_token есть
  // if (authStore.accessToken) {
  //   try {
  //     console.log("✅ Пользователь авторизован, загружаем файлы...");
  //     const response = await getFiles();
  //     files.value = response.data;
  //   } catch (error) {
  //     console.error("❌ Ошибка загрузки файлов:", error);
  //   }
  // } else {
  //   console.warn("⚠️ Нет access_token, файлы не загружаем.");
  // }
};

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (file) {
    await uploadFile(file);
    loadFiles();
  }
};

onMounted(loadFiles);
</script>