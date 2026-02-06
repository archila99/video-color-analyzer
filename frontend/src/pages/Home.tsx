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
    </div>
  )
}
