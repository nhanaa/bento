import { Folders, UserRound } from 'lucide-react'
import React from 'react'

interface TabsProps {
  tab: string
  setTab: (tab: 'folders' | 'settings') => void
}

export const Tabs = ({ tab, setTab }: TabsProps) => {
  return (
    <div className="w-full flex space-x-1 mt-2">
      <button
        onClick={() => setTab('folders')}
        className={`w-1/2 flex items-center justify-center py-2 px-4 rounded-none transition-colors border-0 ${
          tab === 'folders'
            ? 'border-t-2 border-customViolet'
            : 'border-t-2 border-transparent'
        }`}
      >
        <Folders className="w-6 h-6 text-customViolet" />
      </button>
      <button
        onClick={() => setTab('settings')}
        className={`w-1/2 flex items-center justify-center py-2 px-4 rounded-none transition-colors border-0 ${
          tab === 'settings'
            ? 'border-t-2 border-customViolet'
            : 'border-t-2 border-transparent'
        }`}
      >
        <UserRound className="w-6 h-6 text-customViolet" />
      </button>
    </div>
  )
}
