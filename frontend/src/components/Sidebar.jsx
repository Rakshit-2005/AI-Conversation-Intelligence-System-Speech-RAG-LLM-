import React from 'react'
import { FiX } from 'react-icons/fi'

function Sidebar({ isOpen, currentPage, menuItems, onNavigate }) {
  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
          onClick={() => {}}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed left-0 top-0 h-full bg-gradient-to-b from-gray-800 to-gray-900 text-white z-30 transition-all duration-300 lg:static lg:translate-x-0 ${
          isOpen ? 'w-64 translate-x-0' : 'w-64 -translate-x-full'
        }`}
      >
        {/* Logo */}
        <div className="p-6 border-b border-gray-700">
          <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-green-400 bg-clip-text text-transparent">
            ✨ ConvAI
          </h2>
          <p className="text-xs text-gray-400 mt-1">Conversation Intelligence</p>
        </div>

        {/* Menu */}
        <nav className="mt-6 px-3">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = currentPage === item.id
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition duration-200 ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-700'
                }`}
              >
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </button>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-gray-700">
          <div className="bg-gray-700 rounded-lg p-4 text-center">
            <p className="text-xs text-gray-400">API Status</p>
            <p className="text-sm font-semibold text-green-400 mt-1">✓ Connected</p>
          </div>
        </div>
      </div>
    </>
  )
}

export default Sidebar
