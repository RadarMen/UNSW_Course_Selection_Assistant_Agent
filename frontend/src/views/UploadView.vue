<template>
  <main class="upload-page">
    <header class="page-header">
      <div>
        <h1>Handbook 上传</h1>
        <p>上传 PDF 或 TXT 文件，用于后端构建知识库。</p>
      </div>
      <RouterLink class="ghost-button link-button" to="/chat">返回聊天</RouterLink>
    </header>

    <section class="upload-card">
      <label class="file-box">
        <input type="file" accept=".pdf,.txt,application/pdf,text/plain" @change="chooseFile" />
        <strong>{{ file ? file.name : '选择文件' }}</strong>
        <span>支持 PDF、TXT</span>
      </label>

      <button class="primary-button" type="button" :disabled="!file || uploading" @click="upload">
        {{ uploading ? '上传中...' : '上传' }}
      </button>

      <p v-if="error" class="error-text">{{ error }}</p>

      <section v-if="result" class="result-card">
        <h2>上传成功</h2>
        <p><strong>文件：</strong>{{ result.filename }}</p>
        <p><strong>消息：</strong>{{ result.message }}</p>

        <div v-if="result.prerequisites?.length">
          <strong>识别到的先修课：</strong>
          <ul>
            <li v-for="item in result.prerequisites" :key="item">{{ item }}</li>
          </ul>
        </div>
      </section>
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { uploadHandbook } from '../api/upload'

const file = ref(null)
const uploading = ref(false)
const error = ref('')
const result = ref(null)

function chooseFile(event) {
  file.value = event.target.files?.[0] || null
  error.value = ''
  result.value = null
}

async function upload() {
  if (!file.value) {
    return
  }

  uploading.value = true
  error.value = ''
  result.value = null

  try {
    const { data } = await uploadHandbook(file.value)
    if (data.success === false) {
      throw new Error(data.message || '上传失败')
    }
    result.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    uploading.value = false
  }
}
</script>
