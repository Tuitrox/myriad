<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const status = ref('Подтверждение...')

onMounted(async () => {
  const token = route.query.token
  
  if (!token) {
    status.value = 'Ошибка: нет токена'
    return
  }

  try {
    const res = await fetch(`/api/auth/verify?token=${token}`, {
      method: 'POST'
    })
    
    if (res.ok) {
      status.value = 'Почта подтверждена! Перенаправляем...'
      console.log(res.text)
      setTimeout(() => router.push('/login'), 3000)
    } else {
      const err = await res.json()
      status.value = 'Ошибка: ' + err.detail
    }
  } catch (e) {
    status.value = 'Что-то пошло не так'
  }
})
</script>

<template>
  <div class="verify-page">
    <h1>{{ status }}</h1>
  </div>
</template>

<style scoped>
.verify-page { text-align: center; margin-top: 50px; }
</style>