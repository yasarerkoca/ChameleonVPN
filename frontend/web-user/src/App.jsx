import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import UserPanel from './components/UserPanel.jsx'
import ServerSelect from './pages/ServerSelect.jsx'
import Profile from './pages/Profile.jsx'
import Keys from './pages/Keys.jsx'
import Downloads from './pages/Downloads.jsx'

// Not: BrowserRouter zaten src/main.jsx içinde. Burada tekrar sarmalama yok.
export default function App() {
  return (
    <>
      <nav>
        <Link to="/">Home</Link> | <Link to="/servers">Servers</Link> |{' '}
        <Link to="/profile">Profile</Link> | <Link to="/keys">Keys</Link> |{' '}
        <Link to="/downloads">Downloads</Link>
      </nav>

      <Routes>
        <Route
          path="/"
          element={
            <div>
              <h1>Home</h1>
              <UserPanel />
            </div>
          }
        />
        <Route path="/servers" element={<ServerSelect />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/keys" element={<Keys />} />
        <Route path="/downloads" element={<Downloads />} />
      </Routes>
    </>
  )
}
