import { Routes, Route, NavLink } from 'react-router-dom'
import { Home } from './pages/Home'
import { VideoFrames } from './pages/VideoFrames'
import { PhotoSorter } from './pages/PhotoSorter'
import './App.css'

export default function App() {
  return (
    <div className="app">
      <header className="header">
        <NavLink to="/" className={({ isActive }) => `nav-logo ${isActive ? 'active' : ''}`} end>
          Video & Image Processing
        </NavLink>
        <nav className="navbar">
          <NavLink
            to="/video-frames"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            Video Frame Extractor
          </NavLink>
          <NavLink
            to="/photo-sorter"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            Image Identifier
          </NavLink>
        </nav>
      </header>
      <main className="main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/video-frames" element={<VideoFrames />} />
          <Route path="/photo-sorter" element={<PhotoSorter />} />
        </Routes>
      </main>
    </div>
  )
}
