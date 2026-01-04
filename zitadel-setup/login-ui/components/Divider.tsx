import React from 'react'

interface DividerProps {
  text?: string
}

export function Divider({ text = 'or' }: DividerProps) {
  return (
    <div className="divider">
      <span className="divider-text">{text}</span>
    </div>
  )
}

export default Divider
