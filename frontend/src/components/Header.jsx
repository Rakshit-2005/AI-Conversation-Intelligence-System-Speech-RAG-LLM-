import React from 'react'
import { FiMenu, FiBell, FiUser, FiLogOut } from 'react-icons/fi'

function Header({ onToggleSidebar, currentPageLabel }) {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={onToggleSidebar}
            className="p-2 hover:bg-gray-100 rounded-lg transition"
          >
            <FiMenu size={24} />
          </button>
          <h1 className="text-2xl font-bold text-gray-800">
            {currentPageLabel || 'Conversation Intelligence'}
          </h1>
        </div>

        <div className="flex items-center gap-6">
          <button className="p-2 hover:bg-gray-100 rounded-lg transition relative">
            <FiBell size={24} />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          <div className="flex items-center gap-3 pl-6 border-l border-gray-200">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-medium text-gray-800">Admin</p>
              <p className="text-xs text-gray-500">Online</p>
            </div>
            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center">
              <FiUser className="text-white" size={20} />
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
