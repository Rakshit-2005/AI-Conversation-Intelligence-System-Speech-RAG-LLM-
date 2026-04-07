import React, { useState } from 'react'
import { FiCopy, FiDownload, FiRefreshCw } from 'react-icons/fi'
import { apiService } from '../services/api'

function Summarizer() {
  const [text, setText] = useState('')
  const [summaryType, setSummaryType] = useState('full')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSummarize = async () => {
    if (!text.trim()) {
      setError('Please enter text to summarize')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const response = await apiService.summarize(text, summaryType)
      setResult(response.data)
    } catch (err) {
      setError('Failed to summarize text. Make sure API is running and has valid API key.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-800 mb-2">Summarization</h2>
      <p className="text-gray-600 mb-6">Generate intelligent summaries of conversations</p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Input</h3>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Summary Type
            </label>
            <select
              value={summaryType}
              onChange={(e) => setSummaryType(e.target.value)}
              className="input-field"
            >
              <option value="full">Full Summary</option>
              <option value="bullet_points">Bullet Points</option>
              <option value="contextual">Contextual/Business</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Conversation Text
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste your conversation here..."
              className="input-field h-64 resize-none"
            />
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
              {error}
            </div>
          )}

          <button
            onClick={handleSummarize}
            disabled={loading}
            className="btn-primary w-full disabled:opacity-50"
          >
            {loading ? 'Summarizing...' : 'Summarize'}
          </button>
        </div>

        {/* Output */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Summary</h3>

          {result ? (
            <div>
              <div className="bg-gray-50 rounded-lg p-4 mb-4 max-h-96 overflow-auto">
                <p className="text-gray-700 whitespace-pre-wrap">{result.summary}</p>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => navigator.clipboard.writeText(result.summary)}
                  className="flex-1 btn-secondary flex items-center justify-center gap-2"
                >
                  <FiCopy size={16} /> Copy
                </button>
                <button className="flex-1 btn-secondary flex items-center justify-center gap-2">
                  <FiDownload size={16} /> Download
                </button>
                <button
                  onClick={() => setResult(null)}
                  className="flex-1 btn-secondary flex items-center justify-center gap-2"
                >
                  <FiRefreshCw size={16} /> Clear
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-96 text-gray-400">
              <p>Summary will appear here</p>
            </div>
          )}
        </div>
      </div>

      {/* Examples */}
      <div className="mt-8 card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Example Input</h3>
        <p className="text-gray-600 text-sm">
          Try pasting a conversation to see how the summarizer works. For example: "Customer: I need help with my account. Agent: Of course! What's the issue? Customer: I forgot my password..."
        </p>
      </div>
    </div>
  )
}

export default Summarizer
