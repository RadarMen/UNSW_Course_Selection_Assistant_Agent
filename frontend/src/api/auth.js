import http from './http'

export function registerUser(payload) {
  return http.post('/auth/register', payload)
}

export function loginUser(payload) {
  return http.post('/auth/login', payload)
}
