<template>
    <div class="login">
      <h2>Войти в систему</h2>
      <button @click="loginWithGoogle">Войти через Google</button>
    </div>
  </template>
  
  <script setup>
  import { login } from "../api/auth";
  const loginWithGoogle = () => login();
  </script>