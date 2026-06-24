import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ChatView from '../views/ChatView.vue'
import UploadView from '../views/UploadView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/chat', name: 'chat', component: ChatView, meta: { requiresAuth: true } },
    { path: '/upload', name: 'upload', component: UploadView, meta: { requiresAuth: true } }
  ]
})

router.beforeEach((to) => {
  const userId = localStorage.getItem('user_id')
  if (to.meta.requiresAuth && !userId) {
    return '/login'
  }
})

export default router
