import React from 'react'

const Header = ({ title }: { title: string }) => {
  return (
    <header className="w-full flex justify-between items-center py-4 px-8 bg-customViolet">
      <h1 className="w-full text-xl font-semibold text-white text-center">{title}</h1>
    </header>
  )
}

export default Header
