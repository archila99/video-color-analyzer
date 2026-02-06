import { useState, useCallback, useRef } from 'react'
import { apiUrl } from '../api'

interface PhotoAnalysisResult {
  filename: string
  is_colorful: boolean
  colorful_percentage: number
  message: string
}

interface FolderResult {
  total: number
  colorful_count: number
  bw_count: number
  colorful_files: string[]
  bw_files: string[]
}

export function SmartPhotoSorter() {
  const [files, setFiles] = useState<File[]>([])
  const [singleResult, setSingleResult] = useState<PhotoAnalysisResult | null>(null)
  const [folderResult, setFolderResult] = useState<FolderResult | null>(null)
  const [loading, setLoading] = useState<'identify' | 'download' | null>(null)
  const [error, setError] = useState<string | null>(null)

  const fileInputRef = useRef<HTMLInputElement>(null)
  const folderInputRef = useRef<HTMLInputElement>(null)

  const handleAnalyzeSingle = useCallback(async (file: File) => {
    setError(null)
    setSingleResult(null)
    setFolderResult(null)
    setLoading('identify')
    const formData = new FormData()
    formData.append('photo', file)
    try {
      const res = await fetch(apiUrl('/photos/analyze'), { method: 'POST', body: formData })
      if (!res.ok) throw new Error('Analysis failed')
      const data: PhotoAnalysisResult = await res.json()
      setSingleResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Analysis failed')
    } finally {
      setLoading(null)
    }
  }, [])

  const handleAnalyzeMultiple = useCallback(async () => {
    if (files.length === 0) {
      setError('Please select images first')
      return
    }
    setError(null)
    setSingleResult(null)
    setFolderResult(null)
    setLoading('identify')
    const formData = new FormData()
    files.forEach((f) => formData.append('files', f))
    try {
      const res = await fetch(apiUrl('/photos/process-folder'), { method: 'POST', body: formData })
      if (!res.ok) throw new Error('Processing failed')
      const data: FolderResult = await res.json()
      setFolderResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Processing failed')
    } finally {
      setLoading(null)
    }
  }, [files])

  const handleDownloadZip = useCallback(async () => {
    if (files.length === 0) return
    setLoading('download')
    setError(null)
    const formData = new FormData()
    files.forEach((f) => formData.append('files', f))
    try {
      const res = await fetch(apiUrl('/photos/download-sorted'), { method: 'POST', body: formData })
      if (!res.ok) throw new Error('Download failed')
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'sorted_photos.zip'
      a.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Download failed')
    } finally {
      setLoading(null)
    }
  }, [files])

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const list = Array.from(e.target.files || [])
    const images = list.filter((f) => f.type.startsWith('image/'))
    setFiles(images)
    setSingleResult(null)
    setFolderResult(null)
    setError(null)
    if (images.length === 1) handleAnalyzeSingle(images[0])
    e.target.value = ''
  }

  const onFolderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const list = Array.from(e.target.files || [])
    const images = list.filter((f) => f.type.startsWith('image/'))
    setFiles(images)
    setSingleResult(null)
    setFolderResult(null)
    setError(null)
    if (images.length === 1) handleAnalyzeSingle(images[0])
    e.target.value = ''
  }

  const onIdentifyClick = () => {
    if (files.length === 0) {
      setError('Please select images first')
      return
    }
    if (files.length === 1) handleAnalyzeSingle(files[0])
    else handleAnalyzeMultiple()
  }

  const showDownload = files.length > 1 && folderResult !== null

  return (
    <div className={`photo-sorter photo-sorter-compact ${loading ? 'loading' : ''}`}>
      <div className="card card-compact">
        <p className="text-muted">Select one or multiple images to identify (monochrome or color).</p>

        <div
          className={`file-drop-zone file-drop-zone-compact ${files.length > 0 ? 'has-file' : ''}`}
          style={{ pointerEvents: loading ? 'none' : 'auto' }}
        >
          <div className="file-input-wrapper">
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              onChange={onFileChange}
              disabled={!!loading}
            />
            <div className="file-drop-content">
              {files.length > 0 ? (
                <p className="has-file">{files.length} image(s) selected</p>
              ) : (
                <p>
                  Tap to select images{' '}
                  <button
                    type="button"
                    className="link-btn inline"
                    onClick={(e) => {
                      e.stopPropagation()
                      folderInputRef.current?.click()
                    }}
                    disabled={!!loading}
                  >
                    or folder
                  </button>
                </p>
              )}
            </div>
          </div>
          <input
            ref={folderInputRef}
            type="file"
            {...({ webkitDirectory: true } as React.InputHTMLAttributes<HTMLInputElement>)}
            multiple
            onChange={onFolderChange}
            disabled={!!loading}
            style={{ display: 'none' }}
          />
        </div>

        <div className="photo-sorter-actions">
          <button
            className="btn btn-primary"
            onClick={onIdentifyClick}
            disabled={files.length === 0 || !!loading}
          >
            {loading === 'identify' ? 'Identifying...' : 'Identify'}
          </button>
          {showDownload && (
            <button
              className="btn btn-secondary"
              onClick={handleDownloadZip}
              disabled={loading === 'download'}
            >
              {loading === 'download' ? 'Downloading...' : 'Download sorted (color + mono)'}
            </button>
          )}
        </div>

        {singleResult && (
          <div className={`result-badge result-badge-compact ${singleResult.is_colorful ? 'colorful' : 'bw'}`}>
            <strong>{singleResult.message}</strong>
            {singleResult.colorful_percentage.toFixed(1)}% color
          </div>
        )}

        {folderResult && files.length > 1 && (
          <div className="folder-summary">
            <span className="colorful">{folderResult.colorful_count} color</span>
            <span className="sep">·</span>
            <span className="bw">{folderResult.bw_count} mono</span>
          </div>
        )}

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  )
}
