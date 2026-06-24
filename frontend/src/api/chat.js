import http from './http'

export function sendChatMessage(payload) {
  return http.post('/chat', payload)
}

export function getChatHistory(sessionId) {
  return http.get(`/chat/history/${sessionId}`)
}
