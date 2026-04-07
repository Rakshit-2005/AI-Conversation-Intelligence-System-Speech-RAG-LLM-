import React, { useState } from 'react'
import { apiService } from '../services/api'

function ActionItems() {
  const [text, setText] = useState('')
  const [extractionType, setExtractionType] = useState('full')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleExtract = async () => {
    if (!text.trim()) {
      setError('Please enter text to extract action items from')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const response = await apiService.actionItems(text, extractionType)
      setResult(response.data)
    } catch (err) {
      setError('Failed to extract action items.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-800 mb-2">Action Items</h2>
      <p className="text-gray-600 mb-6">Extract tasks, decisions, and follow-ups from conversations</p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Input</h3>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Extraction Type
            </label>
            <select
              value={extractionType}
              onChange={(e) => setExtractionType(e.target.value)}
              className="input-field"
            >
              <option value="full">All Action Items</option>
              <option value="decisions_only">Decisions Only</option>
              <option value="deadlines_only">Deadlines Only</option>
              <option value="risks_only">Risks & Blockers</option>
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
            onClick={handleExtract}
            disabled={loading}
            className="btn-primary w-full disabled:opacity-50"
          >
            {loading ? 'Extracting...' : 'Extract Action Items'}
          </button>
        </div>

        {/* Results */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Extracted Items</h3>

          {result ? (
            <div>
              <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-auto">
                <p className="text-gray-700 whitespace-pre-wrap">{result.items}</p>
              </div>

              <div className="mt-4 flex gap-2">
                <button
                  onClick={() => navigator.clipboard.writeText(result.items)}
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
              <p>Extracted items will appear here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ActionItems
