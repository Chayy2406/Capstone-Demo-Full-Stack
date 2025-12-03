import React, { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [medicineName, setMedicineName] = useState('')
  const [fromCountry, setFromCountry] = useState('US')
  const [toCountry, setToCountry] = useState('India')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const countries = ['US', 'India', 'UK', 'Canada', 'Australia']

  const handleSearch = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('http://localhost:8000/process', {
        original_language: fromCountry,
        requested_language: toCountry,
        original_medication: medicineName
      })

      setResult(response.data)
    } catch (err) {
      if (err.response) {
        setError(err.response.data.detail || 'An error occurred')
      } else {
        setError('Could not connect to the server. Make sure all services are running.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <div className="container">
        <header>
          <h1>Project Codex</h1>
          <p className="subtitle">Medicine Name Translation System</p>
        </header>

        <form onSubmit={handleSearch} className="search-form">
          <div className="form-group">
            <label htmlFor="medicine">Medicine Name</label>
            <input
              id="medicine"
              type="text"
              value={medicineName}
              onChange={(e) => setMedicineName(e.target.value)}
              placeholder="e.g., Tylenol, Advil, Lipitor"
              required
            />
          </div>

          <div className="country-selectors">
            <div className="form-group">
              <label htmlFor="from">From Country</label>
              <select
                id="from"
                value={fromCountry}
                onChange={(e) => setFromCountry(e.target.value)}
              >
                {countries.map(country => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
            </div>

            <div className="arrow">→</div>

            <div className="form-group">
              <label htmlFor="to">To Country</label>
              <select
                id="to"
                value={toCountry}
                onChange={(e) => setToCountry(e.target.value)}
              >
                {countries.map(country => (
                  <option key={country} value={country}>{country}</option>
                ))}
              </select>
            </div>
          </div>

          <button type="submit" disabled={loading} className="search-button">
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        {error && (
          <div className="error-box">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="result-box">
            <h2>Translation Result</h2>
            <div className="result-info">
              <p><strong>Original:</strong> {result.original_medication} ({result.original_language})</p>
              <p><strong>Requested Country:</strong> {result.requested_language}</p>
            </div>

            {result.medication_matches && result.medication_matches.length > 0 ? (
              <div className="matches">
                <h3>Available Medications in {result.requested_language}</h3>
                <div className="match-grid">
                  {result.medication_matches.map((match, index) => (
                    <div key={index} className="match-card">
                      <div className="brand-name">{match.brand}</div>
                      <div className="generic-name">{match.generic}</div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="no-matches">No matching medications found.</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
