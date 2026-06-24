<template>
  <main class="auth-page">
    <section class="auth-card">
      <div class="brand-row">
        <div class="brand-mark">UNSW</div>
        <div>
          <h1>登录</h1>
          <p>进入 UNSW 选课问答助手</p>
        </div>
      </div>

      <form class="form" @submit.prevent="submit">
        <label>
          <span>用户名</span>
          <input v-model.trim="form.username" autocomplete="username" required />
        </label>

        <label>
          <span>密码</span>
          <input v-model="form.password" type="password" autocomplete="current-password" required />
        </label>

        <p v-if="error" class="error-text">{{ error }}</p>

        <button class="primary-button" type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <p class="switch-text">
        没有账号？
        <RouterLink to="/register">注册</RouterLink>
      </p>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginUser } from '../api/auth'
import { saveUser } from '../utils/storage'

const router = useRouter()
const loading = ref(false)
const error = ref('')

const form = reactive({
  username: '',
  password: ''
})

async function submit() {
  loading.value = true
  error.value = ''

  try {
    const { data } = await loginUser({
      username: form.username,
      password: form.password
    })

    if (!data.user?.id) {
      throw new Error('登录成功，但响应中没有 user.id')
    }

    saveUser(data.user)
    await router.push('/chat')
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>
