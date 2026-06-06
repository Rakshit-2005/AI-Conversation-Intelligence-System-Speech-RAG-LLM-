import React, { useState, useRef, useEffect } from 'react'
import { FiUploadCloud, FiCheckCircle, FiAlertTriangle, FiActivity, FiCopy, FiDownload, FiPlay, FiRefreshCw } from 'react-icons/fi'
import { apiService } from '../services/api'

function Transcriber() {
  const [file, setFile] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('') // 'uploading', 'transcribing', 'indexing', 'success', 'error'
  const [error, setError] = useState(null)
  
  // State persistence loading
  const [result, setResult] = useState(() => {
    const saved = localStorage.getItem('transcription_result')
    return saved ? JSON.parse(saved) : null
  })
  
  const [persistedFileName, setPersistedFileName] = useState(() => {
    return localStorage.getItem('transcription_file_name') || ''
  })
  
  const [showFullTranscript, setShowFullTranscript] = useState(false)

  // Direct analysis configuration & state
  const [summaryType, setSummaryType] = useState('full')
  const [sentimentType, setSentimentType] = useState('overall')
  const [actionItemsType, setActionItemsType] = useState('full')

  const [analysisResult, setAnalysisResult] = useState(() => {
    const saved = localStorage.getItem('transcription_analysis')
    return saved ? JSON.parse(saved) : { summary: null, sentiment: null, actionItems: null }
  })

  const [analysisLoading, setAnalysisLoading] = useState({
    summary: false,
    sentiment: false,
    actionItems: false
  })

  const [analysisError, setAnalysisError] = useState({
    summary: null,
    sentiment: null,
    actionItems: null
  })

  // Q&A State
  const [qaQuestion, setQaQuestion] = useState(() => {
    return localStorage.getItem('transcription_qa_question') || ''
  })
  const [qaAnswer, setQaAnswer] = useState(() => {
    return localStorage.getItem('transcription_qa_answer') || ''
  })
  const [qaLoading, setQaLoading] = useState(false)
  const [qaError, setQaError] = useState(null)
  
  const fileInputRef = useRef(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
      setError(null)
    }
  }

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setError(null)
    }
  }

  const onButtonClick = () => {
    fileInputRef.current.click()
  }

  const handleProcess = async (mode) => {
    if (!file) {
      setError('Please select an audio file first')
      return
    }

    try {
      setLoading(true)
      setError(null)
      setResult(null)
      // Clear previous analysis
      setAnalysisResult({ summary: null, sentiment: null, actionItems: null })
      localStorage.removeItem('transcription_analysis')
      
      let newResult = null
      if (mode === 'transcribe_only') {
        setStatus('uploading')
        // Perform upload first
        const uploadRes = await apiService.uploadAudio(file)
        
        setStatus('transcribing')
        // Trigger transcription using filepath
        const transcribeRes = await apiService.transcribe(uploadRes.data.filepath)
        
        newResult = {
          text: transcribeRes.data.text,
          language: transcribeRes.data.language,
          duration: transcribeRes.data.duration,
          indexed: false
        }
      } else {
        setStatus('uploading & processing')
        // Perform end-to-end upload & process
        const processRes = await apiService.processAudioFile(file)
        
        newResult = {
          text: processRes.data.transcription,
          language: 'detected',
          duration: processRes.data.processing_time_seconds,
          indexed: true
        }
      }
      
      setResult(newResult)
      setPersistedFileName(file.name)
      localStorage.setItem('transcription_result', JSON.stringify(newResult))
      localStorage.setItem('transcription_file_name', file.name)
      setStatus('success')
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during audio processing. Make sure python-multipart is installed on the backend.')
      setStatus('error')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleGetAnalysis = async (type) => {
    if (!result || !result.text) return
    
    setAnalysisLoading(prev => ({ ...prev, [type]: true }))
    setAnalysisError(prev => ({ ...prev, [type]: null }))
    
    try {
      let response;
      if (type === 'summary') {
        response = await apiService.summarize(result.text, summaryType)
        setAnalysisResult(prev => {
          const updated = { ...prev, summary: response.data.summary }
          localStorage.setItem('transcription_analysis', JSON.stringify(updated))
          return updated
        })
      } else if (type === 'sentiment') {
        response = await apiService.sentiment(result.text, sentimentType)
        setAnalysisResult(prev => {
          const updated = { ...prev, sentiment: response.data.analysis }
          localStorage.setItem('transcription_analysis', JSON.stringify(updated))
          return updated
        })
      } else if (type === 'actionItems') {
        response = await apiService.actionItems(result.text, actionItemsType)
        setAnalysisResult(prev => {
          const updated = { ...prev, actionItems: response.data.items }
          localStorage.setItem('transcription_analysis', JSON.stringify(updated))
          return updated
        })
      }
    } catch (err) {
      console.error(err)
      setAnalysisError(prev => ({ 
        ...prev, 
        [type]: `Failed to fetch ${type}. Make sure the backend API is running and has a valid API key.`
      }))
    } finally {
      setAnalysisLoading(prev => ({ ...prev, [type]: false }))
    }
  }

  const handleResetAll = () => {
    setFile(null)
    setResult(null)
    setPersistedFileName('')
    setAnalysisResult({ summary: null, sentiment: null, actionItems: null })
    setQaQuestion('')
    setQaAnswer('')
    localStorage.removeItem('transcription_result')
    localStorage.removeItem('transcription_file_name')
    localStorage.removeItem('transcription_analysis')
    localStorage.removeItem('transcription_qa_question')
    localStorage.removeItem('transcription_qa_answer')
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleAskQuestion = async () => {
    if (!qaQuestion.trim() || !result || !result.text) return
    
    setQaLoading(true)
    setQaError(null)
    
    try {
      // Pass the current transcript text as context to answer from this audio conversation
      const response = await apiService.qa(qaQuestion, result.text)
      setQaAnswer(response.data.answer)
      localStorage.setItem('transcription_qa_question', qaQuestion)
      localStorage.setItem('transcription_qa_answer', response.data.answer)
    } catch (err) {
      console.error(err)
      setQaError('Failed to get answer. Make sure the backend API is running and has a valid API key.')
    } finally {
      setQaLoading(false)
    }
  }

  const handleDownload = () => {
    if (!result || !result.text) return
    const blob = new Blob([result.text], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${persistedFileName || 'transcript'}_transcript.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="max-w-4xl mx-auto pb-16">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">🎙️ Audio Transcriber & RAG</h2>
        <p className="text-gray-600">Upload meeting recordings or support calls to transcribe and index them for semantic search</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {/* Upload Zone */}
        <div className="card flex flex-col items-center">
          <form 
            onDragEnter={handleDrag} 
            onDragOver={handleDrag} 
            onDragLeave={handleDrag} 
            onDrop={handleDrop}
            onSubmit={(e) => e.preventDefault()}
            className={`w-full border-2 border-dashed rounded-lg p-8 text-center flex flex-col items-center justify-center transition-all ${
              dragActive ? "border-blue-500 bg-blue-50/50" : "border-gray-300 hover:border-gray-400"
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileChange}
              accept=".mp3,.wav,.m4a,.flac,.ogg"
              className="hidden"
            />
            
            <FiUploadCloud className="w-16 h-16 text-blue-500 mb-4 animate-pulse" />
            
            <p className="text-lg text-gray-700 font-medium mb-1">
              Drag and drop your audio file here, or{" "}
              <button 
                type="button"
                onClick={onButtonClick} 
                className="text-blue-600 hover:underline focus:outline-none"
              >
                browse
              </button>
            </p>
            <p className="text-sm text-gray-500 mb-4">Supports WAV, MP3, M4A, FLAC, OGG</p>

            {file && (
              <div className="bg-blue-50 text-blue-800 rounded px-4 py-2 text-sm font-medium flex items-center gap-2">
                <span>🎵 Selected: {file.name}</span>
                <span className="text-xs text-blue-600">({(file.size / (1024 * 1024)).toFixed(2)} MB)</span>
              </div>
            )}

            {!file && persistedFileName && (
              <div className="bg-gray-100 text-gray-700 rounded px-4 py-2 text-sm font-medium flex items-center gap-2">
                <span>🎵 Last Processed: {persistedFileName}</span>
              </div>
            )}
          </form>

          {error && (
            <div className="w-full mt-4 p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm flex items-center gap-2">
              <FiAlertTriangle className="flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {loading && (
            <div className="w-full mt-6 text-center">
              <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-3"></div>
              <p className="text-gray-700 font-medium capitalize">Status: {status}...</p>
              <p className="text-sm text-gray-500 mt-1">This might take a few moments for large files</p>
            </div>
          )}

          {!loading && file && (
            <div className="w-full mt-6 flex flex-col sm:flex-row gap-4">
              <button
                onClick={() => handleProcess('transcribe_only')}
                className="flex-1 btn-secondary py-3 flex items-center justify-center gap-2 font-medium"
              >
                <FiActivity size={18} /> Transcribe Only
              </button>
              <button
                onClick={() => handleProcess('transcribe_index')}
                className="flex-1 btn-primary py-3 flex items-center justify-center gap-2 font-medium"
              >
                <FiCheckCircle size={18} /> Transcribe & Index (RAG)
              </button>
            </div>
          )}
        </div>

        {/* Results */}
        {result && (
          <div className="card">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b pb-4 mb-4 gap-2">
              <div>
                <h3 className="text-xl font-bold text-gray-800">Transcription Result</h3>
                <div className="flex flex-wrap gap-3 mt-1 text-sm text-gray-600">
                  <span>Language: <strong className="text-gray-800 uppercase">{result.language}</strong></span>
                  <span>•</span>
                  <span>Duration/Time: <strong className="text-gray-800">{typeof result.duration === 'number' ? `${result.duration.toFixed(2)}s` : result.duration}</strong></span>
                  <span>•</span>
                  <span className={`font-semibold ${result.indexed ? 'text-green-600' : 'text-yellow-600'}`}>
                    {result.indexed ? '✓ Indexed in Vector Store' : '⚠ Not Indexed'}
                  </span>
                </div>
              </div>
              
              <div className="flex gap-2 w-full sm:w-auto">
                <button
                  onClick={() => navigator.clipboard.writeText(result.text)}
                  className="flex-1 sm:flex-none btn-secondary py-2 px-4 flex items-center justify-center gap-2"
                >
                  <FiCopy size={16} /> Copy
                </button>
                <button
                  onClick={handleDownload}
                  className="flex-1 sm:flex-none btn-secondary py-2 px-4 flex items-center justify-center gap-2"
                >
                  <FiDownload size={16} /> Download
                </button>
              </div>
            </div>

            <div className={`bg-gray-50 rounded-lg p-5 border overflow-auto transition-all ${
              showFullTranscript ? 'max-h-none' : 'max-h-[400px]'
            }`}>
              <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{result.text}</p>
            </div>
            
            <div className="flex justify-center mt-2 border-b pb-4">
              <button
                onClick={() => setShowFullTranscript(!showFullTranscript)}
                className="text-blue-600 hover:underline text-sm font-medium focus:outline-none"
              >
                {showFullTranscript ? 'Collapse Transcript ↑' : 'Show Full Transcript ↓'}
              </button>
            </div>
            
            {result.indexed && (
              <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-800 text-sm flex items-center gap-2">
                <FiCheckCircle className="text-green-600 flex-shrink-0" size={18} />
                <span>Success! This conversation has been added to the FAISS Vector Database. You can now go to the **Q&A** tab to ask questions about it.</span>
              </div>
            )}

            {/* Integrated Analysis Section */}
            <div className="mt-8 pt-8 border-t border-gray-200">
              <h3 className="text-2xl font-bold text-gray-800 mb-2">⚡ Conversation Intelligence Dashboard</h3>
              <p className="text-gray-600 mb-6 font-normal text-sm">Analyze transcription text directly using summaries, sentiment mapping, and action item extraction.</p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                
                {/* Summarization Card */}
                <div className="border border-gray-200 rounded-xl p-5 flex flex-col justify-between bg-white shadow-sm">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-lg font-bold text-gray-800">Summarizer</h4>
                      <span className="text-xs bg-blue-50 text-blue-800 font-semibold px-2 py-0.5 rounded">LLM</span>
                    </div>
                    
                    <div className="mb-4">
                      <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                        Summary Type
                      </label>
                      <select
                        value={summaryType}
                        onChange={(e) => setSummaryType(e.target.value)}
                        className="input-field py-1.5 text-sm"
                      >
                        <option value="full">Full Summary</option>
                        <option value="bullet_points">Bullet Points</option>
                        <option value="contextual">Contextual/Business</option>
                      </select>
                    </div>
                    
                    {analysisError.summary && (
                      <div className="p-3 mb-4 bg-red-50 border border-red-200 rounded text-red-700 text-xs">
                        {analysisError.summary}
                      </div>
                    )}
                    
                    {analysisResult.summary && (
                      <div className="bg-gray-50 rounded p-3 text-sm text-gray-700 max-h-48 overflow-y-auto mb-4 border whitespace-pre-wrap leading-relaxed">
                        {analysisResult.summary}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-2 mt-4">
                    <button
                      onClick={() => handleGetAnalysis('summary')}
                      disabled={analysisLoading.summary}
                      className="btn-primary py-2 px-3 text-sm flex-1 disabled:opacity-50 flex items-center justify-center gap-1.5"
                    >
                      {analysisLoading.summary ? (
                        <>
                          <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          <span>Generating...</span>
                        </>
                      ) : analysisResult.summary ? 'Regenerate Summary' : 'Generate Summary'}
                    </button>
                    {analysisResult.summary && (
                      <button
                        onClick={() => navigator.clipboard.writeText(analysisResult.summary)}
                        className="btn-secondary py-2 px-3 text-sm flex items-center justify-center"
                        title="Copy Summary"
                      >
                        <FiCopy />
                      </button>
                    )}
                  </div>
                </div>

                {/* Sentiment Card */}
                <div className="border border-gray-200 rounded-xl p-5 flex flex-col justify-between bg-white shadow-sm">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-lg font-bold text-gray-800">Sentiment</h4>
                      <span className="text-xs bg-green-50 text-green-800 font-semibold px-2 py-0.5 rounded">Tone</span>
                    </div>
                    
                    <div className="mb-4">
                      <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                        Analysis Type
                      </label>
                      <select
                        value={sentimentType}
                        onChange={(e) => setSentimentType(e.target.value)}
                        className="input-field py-1.5 text-sm"
                      >
                        <option value="overall">Overall Sentiment</option>
                        <option value="by_speaker">By Speaker</option>
                        <option value="by_topic">By Topic</option>
                        <option value="issues">Issue Detection</option>
                        <option value="satisfaction">Satisfaction</option>
                      </select>
                    </div>
                    
                    {analysisError.sentiment && (
                      <div className="p-3 mb-4 bg-red-50 border border-red-200 rounded text-red-700 text-xs">
                        {analysisError.sentiment}
                      </div>
                    )}
                    
                    {analysisResult.sentiment && (
                      <div className="bg-gray-50 rounded p-3 text-sm text-gray-700 max-h-48 overflow-y-auto mb-4 border whitespace-pre-wrap leading-relaxed">
                        {analysisResult.sentiment}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-2 mt-4">
                    <button
                      onClick={() => handleGetAnalysis('sentiment')}
                      disabled={analysisLoading.sentiment}
                      className="btn-primary py-2 px-3 text-sm flex-1 disabled:opacity-50 flex items-center justify-center gap-1.5"
                    >
                      {analysisLoading.sentiment ? (
                        <>
                          <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          <span>Analyzing...</span>
                        </>
                      ) : analysisResult.sentiment ? 'Regenerate Sentiment' : 'Analyze Sentiment'}
                    </button>
                    {analysisResult.sentiment && (
                      <button
                        onClick={() => navigator.clipboard.writeText(analysisResult.sentiment)}
                        className="btn-secondary py-2 px-3 text-sm flex items-center justify-center"
                        title="Copy Sentiment"
                      >
                        <FiCopy />
                      </button>
                    )}
                  </div>
                </div>

                {/* Action Items Card */}
                <div className="border border-gray-200 rounded-xl p-5 flex flex-col justify-between bg-white shadow-sm">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-lg font-bold text-gray-800">Action Items</h4>
                      <span className="text-xs bg-yellow-50 text-yellow-800 font-semibold px-2 py-0.5 rounded">Tasks</span>
                    </div>
                    
                    <div className="mb-4">
                      <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                        Extraction Type
                      </label>
                      <select
                        value={actionItemsType}
                        onChange={(e) => setActionItemsType(e.target.value)}
                        className="input-field py-1.5 text-sm"
                      >
                        <option value="full">Full Action Plan</option>
                        <option value="decisions_only">Decisions Only</option>
                        <option value="deadlines_only">Deadlines Only</option>
                        <option value="risks_only">Risks & Blockers</option>
                      </select>
                    </div>
                    
                    {analysisError.actionItems && (
                      <div className="p-3 mb-4 bg-red-50 border border-red-200 rounded text-red-700 text-xs">
                        {analysisError.actionItems}
                      </div>
                    )}
                    
                    {analysisResult.actionItems && (
                      <div className="bg-gray-50 rounded p-3 text-sm text-gray-700 max-h-48 overflow-y-auto mb-4 border whitespace-pre-wrap leading-relaxed">
                        {analysisResult.actionItems}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-2 mt-4">
                    <button
                      onClick={() => handleGetAnalysis('actionItems')}
                      disabled={analysisLoading.actionItems}
                      className="btn-primary py-2 px-3 text-sm flex-1 disabled:opacity-50 flex items-center justify-center gap-1.5"
                    >
                      {analysisLoading.actionItems ? (
                        <>
                          <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          <span>Extracting...</span>
                        </>
                      ) : analysisResult.actionItems ? 'Regenerate Actions' : 'Extract Action Items'}
                    </button>
                    {analysisResult.actionItems && (
                      <button
                        onClick={() => navigator.clipboard.writeText(analysisResult.actionItems)}
                        className="btn-secondary py-2 px-3 text-sm flex items-center justify-center"
                        title="Copy Action Items"
                      >
                        <FiCopy />
                      </button>
                    )}
                  </div>
                </div>

              </div>

              {/* Q&A Section */}
              <div className="mt-8 border border-gray-200 rounded-xl p-5 bg-white shadow-sm">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-lg font-bold text-gray-800">Ask Questions about this Conversation</h4>
                  <span className="text-xs bg-purple-50 text-purple-800 font-semibold px-2.5 py-0.5 rounded">Interactive Q&A</span>
                </div>
                
                <div className="mb-4">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={qaQuestion}
                      onChange={(e) => setQaQuestion(e.target.value)}
                      onKeyDown={(e) => { if (e.key === 'Enter') handleAskQuestion() }}
                      placeholder="Ask anything about this recording... (e.g. 'What were the main topics?' or 'What did they decide?')"
                      className="input-field flex-1"
                    />
                    <button
                      onClick={handleAskQuestion}
                      disabled={qaLoading || !qaQuestion.trim()}
                      className="btn-primary px-6 disabled:opacity-50 flex items-center justify-center gap-1.5"
                    >
                      {qaLoading ? (
                        <>
                          <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          <span>Thinking...</span>
                        </>
                      ) : 'Ask'}
                    </button>
                  </div>
                </div>

                {qaError && (
                  <div className="p-3 mb-4 bg-red-50 border border-red-200 rounded text-red-700 text-xs">
                    {qaError}
                  </div>
                )}

                {qaAnswer && (
                  <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-5 border border-purple-100 mt-4 animate-fade-in">
                    <div className="flex justify-between items-start mb-2 border-b pb-2">
                      <h5 className="font-bold text-gray-800 text-sm">Answer:</h5>
                      <button
                        onClick={() => navigator.clipboard.writeText(qaAnswer)}
                        className="text-gray-500 hover:text-blue-600 text-xs flex items-center gap-1"
                        title="Copy Answer"
                      >
                        <FiCopy size={12} /> Copy
                      </button>
                    </div>
                    <p className="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">{qaAnswer}</p>
                  </div>
                )}
              </div>

              {/* Clear All Results Button */}
              <div className="mt-8 text-center pt-4 border-t">
                <button
                  onClick={handleResetAll}
                  className="bg-red-50 hover:bg-red-100 text-red-700 border border-red-200 rounded-lg px-6 py-2.5 font-medium transition-colors inline-flex items-center gap-2"
                >
                  Wipe Transcript & All Analysis
                </button>
              </div>

            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Transcriber
