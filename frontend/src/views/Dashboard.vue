<template>
  <div>
    <header class="dashboard-header">
      <h2>Ваши файлы</h2>
      <button @click="logout" class="logout-btn">Выйти</button>
    </header>

    <input type="file" @change="handleFileUpload" />

    <button @click="deleteAllFilesHandler" class="delete-all-btn" v-if="files.length > 0">
      Удалить все документы
    </button>
    
    <ul>
      <li v-for="file in files" :key="file">
        {{ file }}
        <button @click="deleteFileHandler(file.filename)">Удалить</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { uploadFile, getFiles, deleteFile, deleteAllFiles } from "../api/files";
import { useAuthStore } from "../store/authStore"; // Добавили импорт состояния авторизации

const files = ref([]);
const authStore = useAuthStore(); // Получаем доступ к хранилищу токенов

const loadFiles = async () => {
  console.log("⏳ Проверяем авторизацию перед загрузкой файлов...");

  // Загружаем файлы ТОЛЬКО если access_token есть
  if (authStore.accessToken) {
    try {
      console.log("✅ Пользователь авторизован, загружаем файлы...");
      const response = await getFiles();
      files.value = response.data;
      //console.log(files);
    } catch (error) {
      console.error("❌ Ошибка загрузки файлов:", error);
    }
  } else {
    console.warn("⚠️ Нет access_token, файлы не загружаем.");
  }
};

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (file) {
    await uploadFile(file);
    loadFiles();
  }
};

const deleteFileHandler = async (fileName) => {
  await deleteFile(fileName);
  loadFiles();
};

const deleteAllFilesHandler = async () => {
  await deleteAllFiles();
  files.value = [];
};

const logout = () => {
  authStore.logout();
};

onMounted(loadFiles);
</script>