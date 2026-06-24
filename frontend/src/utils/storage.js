const USER_ID_KEY = 'user_id'
const USERNAME_KEY = 'username'
const SESSION_ID_KEY = 'session_id'

export function saveUser(user) {
  localStorage.setItem(USER_ID_KEY, String(user.id))
  if (user.username) {
    localStorage.setItem(USERNAME_KEY, user.username)
  }
}

export function getUserId() {
  return localStorage.getItem(USER_ID_KEY)
}

export function getUsername() {
  return localStorage.getItem(USERNAME_KEY)
}

export function saveSessionId(sessionId) {
  localStorage.setItem(SESSION_ID_KEY, sessionId)
}

export function getSessionId() {
  return localStorage.getItem(SESSION_ID_KEY)
}

export function clearAuth() {
  localStorage.removeItem(USER_ID_KEY)
  localStorage.removeItem(USERNAME_KEY)
  localStorage.removeItem(SESSION_ID_KEY)
}
