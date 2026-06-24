<template>
  <main class="chat-shell">
    <aside class="sidebar">
      <header class="sidebar-header">
        <div>
          <span class="meta-label">当前用户</span>
          <h2>{{ displayName }}</h2>
        </div>
        <button class="ghost-button" type="button" @click="logout">退出</button>
      </header>

      <button class="primary-button full-button" type="button" :disabled="creating" @click="newSession">
        {{ creating ? '创建中...' : '新建 Session' }}
      </button>

      <section class="session-section">
        <span class="meta-label">会话列表</span>
        <div class="session-list">
          <button
            v-for="session in sessions"
            :key="session.session_id"
            class="session-button"
            :class="{ active: session.session_id === activeSessionId }"
            type="button"
            @click="openSession(session.session_id)"
          >
            <strong>{{ session.title || '新会话' }}</strong>
            <small>{{ formatDate(session.created_at) }}</small>
          </button>
        </div>
      </section>

      <RouterLink class="upload-entry" to="/upload">Handbook 上传</RouterLink>
    </aside>

    <section class="chat-panel">
      <header class="chat-header">
        <div>
          <h1>UNSW Course Assistant</h1>
          <p>{{ activeSessionId || '请选择或新建一个 session' }}</p>
        </div>

        <select v-model="handbookType" class="handbook-select">
          <option value="">自动选择 Handbook</option>
          <option value="course">Course Handbook</option>
          <option value="program">Program Handbook</option>
        </select>
      </header>

      <section class="message-list">
        <div v-if="!messages.length" class="empty-state">
          <h2>开始提问</h2>
          <p>例如：COMP9311 这门课主要学什么？或 AI Master 需要多少学分毕业？</p>
        </div>

        <article
          v-for="(message, index) in messages"
          :key="`${message.role}-${index}-${message.created_at || ''}`"
          class="message"
          :class="message.role === 'user' ? 'from-user' : 'from-ai'"
        >
          <span>{{ message.role === 'user' ? '你' : 'AI' }}</span>
          <p>{{ message.content }}</p>
        </article>
      </section>

      <p v-if="error" class="error-text chat-error">{{ error }}</p>

      <form class="composer" @submit.prevent="send">
        <textarea
          v-model.trim="draft"
          placeholder="输入你的问题..."
          rows="2"
          :disabled="sending || !activeSessionId"
          @keydown.enter.exact.prevent="send"
        />
        <button class="primary-button send-button" type="submit" :disabled="sending || !draft || !activeSessionId">
          {{ sending ? '发送中...' : '发送' }}
        </button>
      </form>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getChatHistory, sendChatMessage } from '../api/chat'
import { createSession, getUserSessions } from '../api/sessions'
import { clearAuth, getSessionId, getUserId, getUsername, saveSessionId } from '../utils/storage'

const router = useRouter()
const userId = getUserId()
const username = getUsername()

const sessions = ref([])
const activeSessionId = ref(getSessionId() || '')
const messages = ref([])
const draft = ref('')
const handbookType = ref('')
const error = ref('')
const creating = ref(false)
const sending = ref(false)

const displayName = computed(() => username || `User ${userId}`)

onMounted(async () => {
  await loadSessions()

  if (activeSessionId.value) {
    await openSession(activeSessionId.value)
    return
  }

  if (sessions.value.length) {
    await openSession(sessions.value[0].session_id)
  }
})

async function loadSessions() {
  error.value = ''

  try {
    const { data } = await getUserSessions(userId)
    sessions.value = data.sessions || []
  } catch (err) {
    error.value = err.message
  }
}

async function newSession() {
  creating.value = true
  error.value = ''

  try {
    const { data } = await createSession(userId)
    const session = {
      session_id: data.session_id,
      title: data.title || '新会话',
      created_at: new Date().toISOString()
    }

    sessions.value = [session, ...sessions.value]
    await openSession(data.session_id)
  } catch (err) {
    error.value = err.message
  } finally {
    creating.value = false
  }
}

async function openSession(sessionId) {
  activeSessionId.value = sessionId
  saveSessionId(sessionId)
  error.value = ''

  try {
    const { data } = await getChatHistory(sessionId)
    messages.value = data.messages || []
  } catch (err) {
    messages.value = []
    error.value = err.message
  }
}

async function send() {
  if (!draft.value || !activeSessionId.value || sending.value) {
    return
  }

  const content = draft.value
  draft.value = ''
  sending.value = true
  error.value = ''

  messages.value.push({
    role: 'user',
    content,
    created_at: new Date().toISOString()
  })

  try {
    const { data } = await sendChatMessage({
      message: content,
      session_id: activeSessionId.value,
      handbook_type: handbookType.value
    })

    messages.value.push({
      role: 'assistant',
      content: data.answer || '后端没有返回 answer',
      created_at: new Date().toISOString()
    })
  } catch (err) {
    error.value = err.message
  } finally {
    sending.value = false
  }
}

function logout() {
  clearAuth()
  router.push('/login')
}

function formatDate(value) {
  if (!value) return ''
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? '' : date.toLocaleDateString()
}
</script>
