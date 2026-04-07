import React, { useState } from 'react'
import { apiService } from '../services/api'

function QA() {
  const [context, setContext] = useState('')
  const [question, setQuestion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAsk = async () => {
    if (!question.trim()) {
      setError('Please enter a question')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const response = await apiService.qa(question, context || undefined)
      setResult(response.data)
    } catch (err) {
      setError('Failed to answer question.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      handleAsk()
    }
  }

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-800 mb-2">Question & Answer</h2>
      <p className="text-gray-600 mb-6">Ask natural language questions about conversations</p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Input */}
        <div className="lg:col-span-2 card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Ask a Question</h3>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Conversation Context (Optional)
            </label>
            <textarea
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Paste conversation context here (or leave empty for RAG search)..."
              className="input-field h-24 resize-none"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Your Question
            </label>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="What do you want to know? (Ctrl+Enter to send)"
              className="input-field h-32 resize-none"
            />
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
              {error}
            </div>
          )}

          <button
            onClick={handleAsk}
            disabled={loading}
            className="btn-primary w-full disabled:opacity-50"
          >
            {loading ? 'Thinking...' : 'Ask Question'}
          </button>
        </div>

        {/* Quick Questions */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Quick Questions</h3>
          <div className="space-y-2">
            {[
              'What are the main topics?',
              'What were the decisions?',
              'Who is responsible?',
              'What are deadlines?',
              'What went wrong?',
              'What\'s next?',
            ].map((q, i) => (
              <button
                key={i}
                onClick={() => setQuestion(q)}
                className="w-full text-left px-3 py-2 rounded border border-gray-200 hover:border-blue-400 hover:bg-blue-50 transition text-sm"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Answer */}
      {result && (
        <div className="mt-6 card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Answer</h3>
          <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-lg p-6 mb-4">
            <p className="text-gray-700 text-lg leading-relaxed">{result.answer}</p>
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => navigator.clipboard.writeText(result.answer)}
              className="btn-secondary flex-1"
            >
              Copy Answer
            </button>
            <button
              onClick={() => setResult(null)}
              className="btn-secondary flex-1"
            >
              Clear
            </button>
          </div>

          {result.sources && result.sources.length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-sm font-medium text-gray-600 mb-2">Relevant Sources:</p>
              <div className="space-y-2">
                {result.sources.map((source, i) => (
                  <div key={i} className="text-xs bg-gray-50 rounded p-2">
                    <p className="text-gray-600">{source.text?.substring(0, 100)}...</p>
                    <p className="text-gray-500 mt-1">Relevance: {(source.similarity_score * 100).toFixed(0)}%</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default QA
