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
  
  const files = ref([]);
  
  const loadFiles = async () => {
    const response = await getFiles();
    files.value = response.data;
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