// pages/index.js
import { useState } from 'react';

export default function Home() {
  const [driver, setDriver] = useState('');
  const [avgLapTime, setAvgLapTime] = useState('');
  const [fastestLap, setFastestLap] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const predict = async () => {
    setError('');
    setResult(null);
    try {
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          driver,
          avg_lap_time: parseFloat(avgLapTime),
          fastest_lap: parseFloat(fastestLap)
        })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Unknown error');
      }
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>🏁 F1 Prediction</h1>
      <input value={driver} onChange={e => setDriver(e.target.value)} placeholder="Driver name" />
      <input value={avgLapTime} onChange={e => setAvgLapTime(e.target.value)} placeholder="Avg Lap Time" />
      <input value={fastestLap} onChange={e => setFastestLap(e.target.value)} placeholder="Fastest Lap Time" />
      <button onClick={predict} style={{ marginTop: '1rem' }}>Predict</button>

      {error && <p style={{color:'red'}}>Error: {error}</p>}
      {result && (
        <div style={{marginTop:'1rem'}}>
          <h2>Prediction:</h2>
          <p>🏆 Top 1 Probability: {(result.Top1_prob * 100).toFixed(2)}%</p>
          <p>🥉 Top 3 Probability: {(result.Top3_prob * 100).toFixed(2)}%</p>
          <p>🖐️ Top 5 Probability: {(result.Top5_prob * 100).toFixed(2)}%</p>
          <p>📈 Predicted Position: {result.FinalPos}</p>
        </div>
      )}
    </div>
  );
}
