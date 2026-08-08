import { useState } from 'react'
import { ingestionApi, IngestionResult, BulkIngestionResult } from '../../services/api/ingestionApi'

export function LogIngestion() {
  const [sourceType, setSourceType] = useState('WINDOWS')
  const [sourceName, setSourceName] = useState('')
  const [rawEvent, setRawEvent] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [ingestionMode, setIngestionMode] = useState<'single' | 'bulk' | 'file'>('single')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<IngestionResult | BulkIngestionResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSingleIngest = async () => {
    if (!rawEvent.trim()) {
      setError('Please enter a raw event')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await ingestionApi.ingestEvent(rawEvent, sourceType, sourceName || undefined)
      setResult(data)
    } catch (err) {
      setError('Failed to ingest event')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleBulkIngest = async () => {
    const events = rawEvent.split('\n').filter(e => e.trim())
    if (events.length === 0) {
      setError('Please enter at least one event')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await ingestionApi.ingestBulk(events, sourceType, sourceName || undefined)
      setResult(data)
    } catch (err) {
      setError('Failed to ingest events')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async () => {
    if (!file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await ingestionApi.uploadFile(file, sourceType, sourceName || undefined)
      setResult(data)
    } catch (err) {
      setError('Failed to upload file')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = () => {
    switch (ingestionMode) {
      case 'single':
        handleSingleIngest()
        break
      case 'bulk':
        handleBulkIngest()
        break
      case 'file':
        handleFileUpload()
        break
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Log Ingestion</h2>
        
        {/* Source Configuration */}
        <div className="space-y-4 mb-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Source Type
              </label>
              <select
                value={sourceType}
                onChange={(e) => setSourceType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="WINDOWS">Windows Security Events</option>
                <option value="LINUX">Linux Authentication Logs</option>
                <option value="FIREWALL">Firewall/Network Logs</option>
                <option value="JSON">Generic JSON Events</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Source Name (optional)
              </label>
              <input
                type="text"
                value={sourceName}
                onChange={(e) => setSourceName(e.target.value)}
                placeholder="e.g., DC01, Firewall-01"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          {/* Ingestion Mode */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Ingestion Mode
            </label>
            <div className="flex gap-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  value="single"
                  checked={ingestionMode === 'single'}
                  onChange={(e) => setIngestionMode(e.target.value as any)}
                  className="mr-2"
                />
                <span className="text-sm">Single Event</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  value="bulk"
                  checked={ingestionMode === 'bulk'}
                  onChange={(e) => setIngestionMode(e.target.value as any)}
                  className="mr-2"
                />
                <span className="text-sm">Bulk (newline-separated)</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  value="file"
                  checked={ingestionMode === 'file'}
                  onChange={(e) => setIngestionMode(e.target.value as any)}
                  className="mr-2"
                />
                <span className="text-sm">File Upload</span>
              </label>
            </div>
          </div>
        </div>

        {/* Input Area */}
        {ingestionMode === 'file' ? (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Upload Log File
            </label>
            <input
              type="file"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              accept=".log,.txt,.json,.jsonl"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-xs text-gray-500 mt-1">
              Max file size: 10MB. Supported formats: .log, .txt, .json, .jsonl
            </p>
          </div>
        ) : (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {ingestionMode === 'single' ? 'Raw Event' : 'Raw Events (one per line)'}
            </label>
            <textarea
              value={rawEvent}
              onChange={(e) => setRawEvent(e.target.value)}
              placeholder={
                ingestionMode === 'single'
                  ? 'Paste a single log event here...'
                  : 'Paste multiple log events, one per line...'
              }
              rows={ingestionMode === 'single' ? 6 : 12}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono text-sm"
            />
          </div>
        )}

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {loading ? 'Processing...' : ingestionMode === 'file' ? 'Upload File' : 'Ingest Events'}
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Result Display */}
      {result && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-green-900 mb-4">Ingestion Result</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded p-3 border border-green-200">
              <div className="text-2xl font-bold text-green-900">
                {result.received}
              </div>
              <div className="text-sm text-green-700">Received</div>
            </div>
            <div className="bg-white rounded p-3 border border-green-200">
              <div className="text-2xl font-bold text-green-900">
                {result.parsed}
              </div>
              <div className="text-sm text-green-700">Parsed</div>
            </div>
            <div className="bg-white rounded p-3 border border-green-200">
              <div className="text-2xl font-bold text-green-900">
                {result.normalized}
              </div>
              <div className="text-sm text-green-700">Normalized</div>
            </div>
            <div className="bg-white rounded p-3 border border-green-200">
              <div className="text-2xl font-bold text-green-900">
                {result.stored}
              </div>
              <div className="text-sm text-green-700">Stored</div>
            </div>
            <div className="bg-white rounded p-3 border border-green-200">
              <div className="text-2xl font-bold text-green-900">
                {result.enriched}
              </div>
              <div className="text-sm text-green-700">Enriched</div>
            </div>
            <div className="bg-white rounded p-3 border border-green-200">
              <div className="text-2xl font-bold text-green-900">
                {result.alerts_generated}
              </div>
              <div className="text-sm text-green-700">Alerts Generated</div>
            </div>
            <div className="bg-white rounded p-3 border border-green-200">
              <div className="text-2xl font-bold text-green-900">
                {result.incidents_created}
              </div>
              <div className="text-sm text-green-700">Incidents Created</div>
            </div>
            <div className="bg-white rounded p-3 border border-green-200">
              <div className="text-2xl font-bold text-red-900">
                {result.rejected}
              </div>
              <div className="text-sm text-red-700">Rejected</div>
            </div>
          </div>

          {'processing_time_ms' in result && (
            <div className="mt-4 text-sm text-gray-600">
              Processing time: {result.processing_time_ms}ms
            </div>
          )}

          {result.errors && result.errors.length > 0 && (
            <div className="mt-4">
              <h4 className="text-sm font-medium text-red-900 mb-2">Errors:</h4>
              <ul className="text-sm text-red-700 list-disc list-inside">
                {result.errors.map((error, idx) => (
                  <li key={idx}>{error}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
