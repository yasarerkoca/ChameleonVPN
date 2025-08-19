import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import UserPanel from './components/UserPanel';
import ServerSelect from './pages/ServerSelect';
import Profile from './pages/Profile';
import Keys from './pages/Keys';
import Downloads from './pages/Downloads';

/**
 * Root application component for the web user portal.
 * Provides routing to user features such as server selection,
 * profile management, key retrieval and configuration downloads.
 */
function App() {
  return (
    <BrowserRouter>
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
    </BrowserRouter>
  );
}

export default App;
