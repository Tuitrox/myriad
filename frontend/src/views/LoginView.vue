<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const email = ref('')
const password = ref('')

const handleSubmit = () => {
  authStore.login({
    email: email.value,
    password: password.value
  })
}
</script>

<template>
  <div class="auth-page">
    <h1>Вход</h1>
    <form @submit.prevent="handleSubmit">
      <div class="field">
        <label>Email:</label>
        <input v-model="email" type="text" required placeholder="user@example.com" />
      </div>
      
      <div class="field">
        <label>Пароль:</label>
        <input v-model="password" type="password" required />
      </div>

      <button type="submit">Войти</button>
    </form>
    
    <p>Нет аккаунта? <RouterLink to="/register">Регистрация</RouterLink></p>
  </div>
</template>

<style scoped>
.auth-page { max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }
.field { margin-bottom: 15px; display: flex; flex-direction: column; }
input { padding: 8px; margin-top: 5px; }
button { padding: 10px; background: #42b983; color: white; border: none; cursor: pointer; }
</style>