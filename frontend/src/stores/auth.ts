import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  

  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(formData: any) {
    try {
      const params = new URLSearchParams()
      params.append('username', formData.email) 
      params.append('password', formData.password)

      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' 
        },
        body: params
      })

      if (!response.ok) {
         const errorData = await response.json()
         throw new Error(errorData.detail || 'Ошибка логина')
      }

      const data = await response.json()
      
      token.value = data.access_token 
      localStorage.setItem('token', data.access_token)
      
      router.push('/')
      
    } catch (e: any) {
      alert(e.message)
      console.error(e)
    }
  }

  async function register(formData: any) {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Ошибка регистрации')
      }

      alert('Письмо отправлено!')
      
    } catch (e: any) {
      alert(e.message)
    }
  }

  function logout() {
    token.value = ''
    localStorage.removeItem('token')
    router.push('/login')
  }

  return { token, isAuthenticated, login, register, logout }
})