import { useState, useCallback, useEffect } from 'react'
import { apiUrl } from '../api'

interface VideoMetadata {
  duration: number
  fps: number
  size: number[]
}

export function VideoFrameExtractor() {
  const [videoFile, setVideoFile] = useState<File | null>(null)
  const [metadata, setMetadata] = useState<VideoMetadata | null>(null)
  const [startTime, setStartTime] = useState(0)
  const [endTime, setEndTime] = useState(10)
  const [interval, setInterval] = useState(0.1)
  const [overlayTime, setOverlayTime] = useState(false)
  const [removeShadows, setRemoveShadows] = useState(false)
  const [loading, setLoading] = useState(false)
  const [extractedZipUrl, setExtractedZipUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const maxInterval = Math.round((endTime - startTime) * 100) / 100

  useEffect(() => {
    return () => {
      if (extractedZipUrl) URL.revokeObjectURL(extractedZipUrl)
    }
  }, [extractedZipUrl])

  const handleFileSelect = useCallback(async (file: File) => {
    if (!file.type.startsWith('video/')) {
      setError('Please select a video file')
      return
    }
    setError(null)
    setVideoFile(file)
    setMetadata(null)
    if (extractedZipUrl) {
      URL.revokeObjectURL(extractedZipUrl)
      setExtractedZipUrl(null)
    }

    const formData = new FormData()
    formData.append('video', file)
    try {
      const res = await fetch(apiUrl('/video-metadata'), {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error('Failed to get metadata')
      const data: VideoMetadata = await res.json()
      setMetadata(data)
      setStartTime(0)
      setEndTime(Math.round(data.duration * 100) / 100)
      setInterval(0.1)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to analyze video')
    }
  }, [extractedZipUrl])

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      const file = e.dataTransfer.files[0]
      if (file) handleFileSelect(file)
    },
    [handleFileSelect]
  )

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    ;(e.currentTarget as HTMLElement).classList.add('dragover')
  }

  const onDragLeave = (e: React.DragEvent) => {
    (e.currentTarget as HTMLElement).classList.remove('dragover')
  }

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) handleFileSelect(file)
  }

  const handleExtract = async () => {
    if (!videoFile) {
      setError('Please select a video first')
      return
    }
    if (!metadata) return

    const duration = metadata.duration
    if (startTime < 0) {
      setError('Start time cannot be less than 0')
      return
    }
    if (startTime > endTime) {
      setError('Start time cannot be greater than end time')
      return
    }
    if (endTime > duration) {
      setError(`End time (${endTime}) cannot exceed video duration (${duration}s)`)
      return
    }
    if (interval > maxInterval) {
      setError(`Interval (${interval}) cannot exceed end − start (${maxInterval.toFixed(2)})`)
      return
    }

    setLoading(true)
    setError(null)
    if (extractedZipUrl) {
      URL.revokeObjectURL(extractedZipUrl)
      setExtractedZipUrl(null)
    }
    const formData = new FormData()
    formData.append('video', videoFile)
    formData.append('start_time', String(startTime))
    formData.append('end_time', String(endTime))
    formData.append('interval', String(Math.min(interval, maxInterval)))
    formData.append('overlay_time', String(overlayTime))
    formData.append('remove_shadows', String(removeShadows))

    try {
      const res = await fetch(apiUrl('/extract-frames'), {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error('Failed to extract frames')
      const blob = await res.blob()
      setExtractedZipUrl(URL.createObjectURL(blob))
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Extraction failed')
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (!extractedZipUrl) return
    const a = document.createElement('a')
    a.href = extractedZipUrl
    a.download = 'frames.zip'
    a.click()
  }

  return (
    <div className={`video-extractor ${loading ? 'loading' : ''}`}>
      <div className="card">
        <h2>Select Video</h2>
        <div
          className="file-drop-zone"
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          style={{ cursor: 'pointer' }}
        >
          <div className="file-input-wrapper">
            <input type="file" accept="video/*" onChange={onFileChange} />
            {videoFile ? (
              <p className="has-file">
                <strong>{videoFile.name}</strong>
                {metadata && (
                  <span className="meta">
                    {' '}
                    • {metadata.duration}s • {metadata.size[0]}×{metadata.size[1]}
                  </span>
                )}
              </p>
            ) : (
              <p>Drop a video here or click to browse</p>
            )}
          </div>
        </div>
        {error && <p className="error">{error}</p>}
      </div>

      {metadata && (
        <>
          <div className="card">
            <h2>Time Range</h2>
            <div className="form-row">
              <div className="form-group">
                <label>Start Time (seconds)</label>
                <input
                  type="number"
                  min={0}
                  max={metadata.duration}
                  step={0.1}
                  value={startTime}
                  onChange={(e) => setStartTime(Number(e.target.value))}
                />
              </div>
              <div className="form-group">
                <label>End Time (seconds)</label>
                <input
                  type="number"
                  min={0}
                  max={metadata.duration}
                  step={0.1}
                  value={endTime}
                  onChange={(e) => setEndTime(Number(e.target.value))}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Interval (seconds) — max {maxInterval.toFixed(2)}</label>
              <input
                type="number"
                min={0.01}
                step={0.2}
                value={interval}
                onChange={(e) => {
                  const val = Number(e.target.value) || 0
                  setInterval(val === 0 ? 0 : Math.round(val * 100) / 100)
                }}
              />
              {interval > maxInterval && (
                <p className="error" style={{ marginTop: '0.5rem' }}>
                  Interval ({interval}) is greater than end − start ({maxInterval.toFixed(2)})
                </p>
              )}
            </div>
          </div>
          <div className="card">
            <h2>Options</h2>
            <div className="checkbox-group">
              <input
                type="checkbox"
                id="overlay"
                checked={overlayTime}
                onChange={(e) => setOverlayTime(e.target.checked)}
              />
              <label htmlFor="overlay">Overlay timestamp on frames</label>
            </div>
            <div className="checkbox-group">
              <input
                type="checkbox"
                id="shadows"
                checked={removeShadows}
                onChange={(e) => setRemoveShadows(e.target.checked)}
              />
              <label htmlFor="shadows">Remove shadows / brighten dark areas</label>
            </div>
          </div>
          <div className="card" style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <button
              className="btn btn-primary"
              onClick={handleExtract}
              disabled={loading}
            >
              {loading ? 'Extracting...' : 'Extract Frames'}
            </button>
            {extractedZipUrl && (
              <button className="btn btn-secondary" onClick={handleDownload}>
                Download frames.zip
              </button>
            )}
          </div>
        </>
      )}
    </div>
  )
}
