import React from 'react'
import ReactDOM from 'react-dom/client'
import FileList from './FileList'

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
)
root.render(
  <React.StrictMode>
    <FileList />
  </React.StrictMode>
)
