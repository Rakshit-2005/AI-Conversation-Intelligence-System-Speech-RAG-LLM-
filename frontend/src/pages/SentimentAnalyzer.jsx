import React, { useState } from 'react'
import { apiService } from '../services/api'

function SentimentAnalyzer() {
  const [text, setText] = useState('')
  const [analysisType, setAnalysisType] = useState('overall')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter text to analyze')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const response = await apiService.sentiment(text, analysisType)
      setResult(response.data)
    } catch (err) {
      setError('Failed to analyze sentiment.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getSentimentColor = (sentiment) => {
    if (!sentiment) return 'gray'
    if (sentiment.toLowerCase().includes('positive')) return 'green'
    if (sentiment.toLowerCase().includes('negative')) return 'red'
    return 'yellow'
  }

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-800 mb-2">Sentiment Analysis</h2>
      <p className="text-gray-600 mb-6">Analyze emotional tone and sentiment of conversations</p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Input</h3>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Analysis Type
            </label>
            <select
              value={analysisType}
              onChange={(e) => setAnalysisType(e.target.value)}
              className="input-field"
            >
              <option value="overall">Overall Sentiment</option>
              <option value="by_speaker">By Speaker</option>
              <option value="by_topic">By Topic</option>
              <option value="issues">Issue Detection</option>
              <option value="satisfaction">Satisfaction</option>
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
            onClick={handleAnalyze}
            disabled={loading}
            className="btn-primary w-full disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze Sentiment'}
          </button>
        </div>

        {/* Results */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Analysis Result</h3>

          {result ? (
            <div>
              <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-auto">
                <p className="text-gray-700 whitespace-pre-wrap">{result.analysis}</p>
              </div>

              <div className="mt-4 flex gap-2">
                <button
                  onClick={() => navigator.clipboard.writeText(result.analysis)}
                  className="btn-secondary flex-1"
                >
                  Copy
                </button>
                <button
                  onClick={() => setResult(null)}
                  className="btn-secondary flex-1"
                >
                  Clear
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-96 text-gray-400">
              <p>Analysis will appear here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default SentimentAnalyzer
