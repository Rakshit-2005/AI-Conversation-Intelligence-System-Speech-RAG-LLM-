import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  // Health Check
  getHealth: () => api.get('/health'),

  // Transcription
  transcribe: (audioPath, language = 'en') =>
    api.post('/transcribe', { audio_path: audioPath, language }),

  // Processing
  processConversation: (audioPath, language = 'en') =>
    api.post('/process-conversation', { audio_path: audioPath, language }),

  // Retrieval
  retrieve: (query, topK = 5, threshold = 0.3) =>
    api.post('/retrieve', { query, top_k: topK, threshold }),

  // Analysis
  summarize: (text, type = 'full') =>
    api.post('/summarize', { text, type }),

  sentiment: (text, analysisType = 'overall') =>
    api.post('/sentiment', { text, analysis_type: analysisType }),

  actionItems: (text, extractionType = 'full') =>
    api.post('/action-items', { text, extraction_type: extractionType }),

  qa: (question, context = null) =>
    api.post('/qa', { question, context }),

  searchExplain: (query, topK = 5) =>
    api.post('/search-explain', { query, top_k: topK }),

  analyze: (text, includeAll = true) =>
    api.post('/analyze', {
      text,
      include_summary: includeAll,
      include_sentiment: includeAll,
      include_action_items: includeAll,
      include_themes: includeAll,
      include_risks: includeAll,
    }),
  
  // Audio Upload
  uploadAudio: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  processAudioFile: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/process-audio-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // Vector Store
  getVectorStoreStats: () => api.get('/vector-store/stats'),

  clearVectorStore: () => api.post('/vector-store/clear'),
}

export default api
