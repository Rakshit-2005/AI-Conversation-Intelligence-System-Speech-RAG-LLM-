import React from 'react'

function StatusCard({ icon: Icon, title, value, description, color = 'blue' }) {
  const colorClass = {
    blue: 'bg-blue-50 text-blue-600 border-blue-200',
    green: 'bg-green-50 text-green-600 border-green-200',
    yellow: 'bg-yellow-50 text-yellow-600 border-yellow-200',
    red: 'bg-red-50 text-red-600 border-red-200',
  }[color]

  return (
    <div className={`card border-2 ${colorClass}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
          {description && (
            <p className="text-xs text-gray-500 mt-1">{description}</p>
          )}
        </div>
        {Icon && (
          <div className="text-4xl opacity-20">
            <Icon size={40} />
          </div>
        )}
      </div>
    </div>
  )
}

export default StatusCard
