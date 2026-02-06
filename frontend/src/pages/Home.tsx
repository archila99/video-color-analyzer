import { Link } from 'react-router-dom'

export function Home() {
  return (
    <div className="home-page">
      <section className="hero">
        <h1>Video & Image Processing</h1>
        <p className="hero-subtitle">
          Extract frames from videos and identify color vs monochrome images.
        </p>
      </section>

      <section className="services">
        <h2>Services</h2>
        <div className="service-cards">
          <Link to="/video-frames" className="service-card">
            <h3>Video Frame Extractor</h3>
            <p>
              Upload a video and extract frames within a time range. Configure interval, overlay
              timestamps, and apply shadow removal. Download all frames as a ZIP file.
            </p>
            <span className="service-link">Use service →</span>
          </Link>
          <Link to="/photo-sorter" className="service-card">
            <h3>Image Identifier</h3>
            <p>
              Select one or multiple images to identify if they are color or monochrome. For batch
              uploads, download sorted folders (color and mono) as a ZIP.
            </p>
            <span className="service-link">Use service →</span>
          </Link>
        </div>
      </section>

      <section className="api-info">
        <h2>API Endpoints</h2>
        <ul className="endpoint-list">
          <li>
            <code>POST /video-metadata</code> — Get video duration, fps, and dimensions
          </li>
          <li>
            <code>POST /extract-frames</code> — Extract frames from video (returns ZIP)
          </li>
          <li>
            <code>POST /photos/analyze</code> — Analyze single image (color vs monochrome)
          </li>
          <li>
            <code>POST /photos/process-folder</code> — Process multiple images, returns classification
          </li>
          <li>
            <code>POST /photos/download-sorted</code> — Process and download sorted images as ZIP
          </li>
          <li>
            <code>GET /health</code> — Health check
          </li>
        </ul>
      </section>
    </div>
  )
}
