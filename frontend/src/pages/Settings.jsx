import React, { useState, useEffect } from 'react'
import { FiRefreshCw, FiTrash2, FiCheck } from 'react-icons/fi'
import { apiService } from '../services/api'

function Settings() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [clearing, setClearing] = useState(false)
  const [message, setMessage] = useState(null)

  const fetchStats = async () => {
    try {
      setLoading(true)
      const response = await apiService.getVectorStoreStats()
      setStats(response.data)
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to fetch stats' })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStats()
  }, [])

  const handleClearIndex = async () => {
    if (!window.confirm('Are you sure? This will delete all indexed data.')) return

    try {
      setClearing(true)
      await apiService.clearVectorStore()
      setMessage({ type: 'success', text: 'Vector store cleared successfully' })
      await fetchStats()
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to clear vector store' })
    } finally {
      setClearing(false)
    }
  }

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-800 mb-2">Settings</h2>
      <p className="text-gray-600 mb-6">System configuration and management</p>

      {message && (
        <div
          className={`mb-4 p-4 rounded-lg flex items-center gap-2 ${
            message.type === 'success'
              ? 'bg-green-50 text-green-800 border border-green-200'
              : 'bg-red-50 text-red-800 border border-red-200'
          }`}
        >
          {message.type === 'success' && <FiCheck />}
          {message.text}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Vector Store Stats */}
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Vector Store</h3>
            <button
              onClick={fetchStats}
              disabled={loading}
              className="p-2 hover:bg-gray-100 rounded transition"
            >
              <FiRefreshCw size={20} className={loading ? 'animate-spin' : ''} />
            </button>
          </div>

          {stats ? (
            <div className="space-y-4">
              <div className="flex justify-between pb-3 border-b border-gray-200">
                <span className="text-gray-600">Total Entries:</span>
                <span className="font-semibold text-lg">{stats.total_entries}</span>
              </div>
              <div className="flex justify-between pb-3 border-b border-gray-200">
                <span className="text-gray-600">Dimension:</span>
                <span className="font-semibold">{stats.dimension}</span>
              </div>
              <div className="flex justify-between pb-3 border-b border-gray-200">
                <span className="text-gray-600">Index Type:</span>
                <span className="font-semibold">{stats.index_type}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Status:</span>
                <span className="font-semibold text-green-600">✓ Active</span>
              </div>

              <button
                onClick={handleClearIndex}
                disabled={clearing}
                className="w-full mt-6 flex items-center justify-center gap-2 bg-red-50 hover:bg-red-100 text-red-600 font-semibold py-2 px-4 rounded-lg transition disabled:opacity-50"
              >
                <FiTrash2 size={20} />
                {clearing ? 'Clearing...' : 'Clear Vector Store'}
              </button>
            </div>
          ) : (
            <div className="text-gray-500 text-center py-8">Loading...</div>
          )}
        </div>

        {/* API Configuration */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">API Configuration</h3>

          <div className="space-y-4">
            <div className="pb-3 border-b border-gray-200">
              <p className="text-sm text-gray-600">Base URL</p>
              <p className="font-semibold text-gray-800 mt-1">http://localhost:8000</p>
            </div>

            <div className="pb-3 border-b border-gray-200">
              <p className="text-sm text-gray-600">Frontend URL</p>
              <p className="font-semibold text-gray-800 mt-1">http://localhost:3000</p>
            </div>

            <div className="pb-3 border-b border-gray-200">
              <p className="text-sm text-gray-600">Environment</p>
              <p className="font-semibold text-gray-800 mt-1">Development</p>
            </div>

            <div>
              <p className="text-sm text-gray-600">Status</p>
              <div className="flex items-center gap-2 mt-1">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <p className="font-semibold text-green-600">Connected</p>
              </div>
            </div>

            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary w-full text-center mt-6"
            >
              View API Documentation
            </a>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="mt-6 card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Enabled Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {[
            'Speech Recognition',
            'Text Chunking',
            'Embeddings',
            'Vector Search',
            'Summarization',
            'Sentiment Analysis',
            'Action Extraction',
            'Question Answering',
            'RAG Pipeline',
          ].map((feature, i) => (
            <div key={i} className="flex items-center gap-2 p-2 bg-green-50 rounded border border-green-200">
              <FiCheck className="text-green-600" />
              <span className="text-sm text-gray-700">{feature}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Settings
