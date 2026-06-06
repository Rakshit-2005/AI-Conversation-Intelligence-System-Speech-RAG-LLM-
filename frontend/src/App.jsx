import React, { useState, useEffect } from 'react'
import { FiHome, FiFileText, FiSmile, FiCheckCircle, FiHelpCircle, FiSettings, FiServer, FiMic } from 'react-icons/fi'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Summarizer from './pages/Summarizer'
import SentimentAnalyzer from './pages/SentimentAnalyzer'
import ActionItems from './pages/ActionItems'
import QA from './pages/QA'
import Settings from './pages/Settings'
import Transcriber from './pages/Transcriber'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: FiHome },
    { id: 'transcribe', label: 'Transcribe Audio', icon: FiMic },
    { id: 'summarizer', label: 'Summarizer', icon: FiFileText },
    { id: 'sentiment', label: 'Sentiment', icon: FiSmile },
    { id: 'actions', label: 'Action Items', icon: FiCheckCircle },
    { id: 'qa', label: 'Q&A', icon: FiHelpCircle },
    { id: 'settings', label: 'Settings', icon: FiSettings },
  ]

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />
      case 'transcribe':
        return <Transcriber />
      case 'summarizer':
        return <Summarizer />
      case 'sentiment':
        return <SentimentAnalyzer />
      case 'actions':
        return <ActionItems />
      case 'qa':
        return <QA />
      case 'settings':
        return <Settings />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar 
        isOpen={sidebarOpen} 
        currentPage={currentPage}
        menuItems={menuItems}
        onNavigate={setCurrentPage}
      />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header 
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          currentPageLabel={menuItems.find(item => item.id === currentPage)?.label}
        />
        
        <main className="flex-1 overflow-auto">
          <div className="container-custom py-8">
            {renderPage()}
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
