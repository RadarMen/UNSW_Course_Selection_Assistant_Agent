<template>
  <main class="auth-page">
    <section class="auth-card">
      <div class="brand-row">
        <div class="brand-mark">UNSW</div>
        <div>
          <h1>注册</h1>
          <p>创建账号后使用聊天和上传功能</p>
        </div>
      </div>

      <form class="form" @submit.prevent="submit">
        <label>
          <span>用户名</span>
          <input v-model.trim="form.username" autocomplete="username" required />
        </label>

        <label>
          <span>邮箱</span>
          <input v-model.trim="form.email" type="email" autocomplete="email" required />
        </label>

        <label>
          <span>密码</span>
          <input v-model="form.password" type="password" autocomplete="new-password" required />
        </label>

        <p v-if="error" class="error-text">{{ error }}</p>
        <p v-if="success" class="success-text">{{ success }}</p>

        <button class="primary-button" type="submit" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <p class="switch-text">
        已有账号？
        <RouterLink to="/login">登录</RouterLink>
      </p>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '../api/auth'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const success = ref('')

const form = reactive({
  username: '',
  email: '',
  password: ''
})

async function submit() {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    await registerUser({
      username: form.username,
      email: form.email,
      password: form.password
    })
    success.value = '注册成功，正在返回登录页...'
    setTimeout(() => router.push('/login'), 700)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>
