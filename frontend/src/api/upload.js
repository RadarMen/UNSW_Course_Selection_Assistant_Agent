import http from './http'

export function uploadHandbook(file) {
  const formData = new FormData()
  formData.append('file', file)

  return http.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
