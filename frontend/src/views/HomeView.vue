<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>

<template>
  <main>
    <h1>Привет! Это секретная страница 🤫</h1>
    <p>Твой токен: {{ authStore.token.slice(0, 10) }}...</p>
    <button @click="authStore.logout">Выйти</button>
  </main>
</template>