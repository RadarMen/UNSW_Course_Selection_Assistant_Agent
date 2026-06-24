import http from './http'

export function createSession(userId) {
  return http.post('/session/create', {
    user_id: Number(userId)
  })
}

export function getUserSessions(userId) {
  return http.get(`/user/${userId}/sessions`)
}
