import React, { useState, useEffect } from 'react'
import { FiServer, FiDatabase, FiCpu, FiActivity } from 'react-icons/fi'
import StatusCard from '../components/StatusCard'
import { apiService } from '../services/api'

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [health, setHealth] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [healthRes, statsRes] = await Promise.all([
        apiService.getHealth(),
        apiService.getVectorStoreStats(),
      ])
      setHealth(healthRes.data)
      setStats(statsRes.data)
      setError(null)
    } catch (err) {
      setError('Failed to fetch system data')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="mb-4">
            <div className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto"></div>
          </div>
          <p className="text-gray-600">Loading system information...</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">Dashboard</h2>
        <p className="text-gray-600">Overview of your Conversation Intelligence System</p>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatusCard
          icon={FiServer}
          title="System Status"
          value={health?.status === 'healthy' ? 'Online' : 'Offline'}
          description="API Status"
          color={health?.status === 'healthy' ? 'green' : 'red'}
        />
        <StatusCard
          icon={FiDatabase}
          title="Vector Store"
          value={stats?.total_entries || 0}
          description="Indexed entries"
          color="blue"
        />
        <StatusCard
          icon={FiCpu}
          title="LLM Provider"
          value={health?.llm_provider?.toUpperCase() || 'N/A'}
          description="Active provider"
          color="yellow"
        />
        <StatusCard
          icon={FiActivity}
          title="API Health"
          value={health?.embeddings_ready ? '✓' : '✗'}
          description="Models loaded"
          color={health?.embeddings_ready ? 'green' : 'red'}
        />
      </div>

      {/* System Information */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* API Info */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">API Information</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Status:</span>
              <span className="font-medium text-green-600">✓ Connected</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Version:</span>
              <span className="font-medium">{health?.version || 'N/A'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Provider:</span>
              <span className="font-medium">{health?.llm_provider || 'N/A'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Endpoint:</span>
              <span className="font-medium text-blue-600">localhost:8000</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="btn-primary w-full text-left">📝 Summarize Conversation</button>
            <button className="btn-primary w-full text-left">😊 Analyze Sentiment</button>
            <button className="btn-primary w-full text-left">✅ Extract Action Items</button>
            <button className="btn-primary w-full text-left">💬 Ask Questions</button>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="mt-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">Available Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            { title: '🎙️ Transcription', desc: 'Convert audio to text' },
            { title: '📚 Chunking', desc: 'Intelligent text segmentation' },
            { title: '🔢 Embeddings', desc: 'Vector representation' },
            { title: '🔍 RAG Search', desc: 'Semantic retrieval' },
            { title: '📝 Summarization', desc: '4 summary types' },
            { title: '😊 Sentiment', desc: '5 analysis types' },
            { title: '✅ Actions', desc: 'Task extraction' },
            { title: '💬 Q&A', desc: 'Intelligent questioning' },
            { title: '🚀 API', desc: '13 endpoints' },
          ].map((feature, idx) => (
            <div key={idx} className="card">
              <p className="font-semibold text-gray-800">{feature.title}</p>
              <p className="text-sm text-gray-600 mt-1">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
