// frontend/pages/index.js
import { useState } from 'react';

export default function Home() {
  const [form, setForm] = useState({
    driver: '',
    avg_lap_time: '',
    fastest_lap: ''
  });
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>F1 Prediction</h1>
      <form onSubmit={handleSubmit}>
        <input placeholder="Driver" value={form.driver} onChange={e => setForm({...form, driver: e.target.value})} /><br />
        <input placeholder="Avg Lap Time" type="number" value={form.avg_lap_time} onChange={e => setForm({...form, avg_lap_time: e.target.value})} /><br />
        <input placeholder="Fastest Lap" type="number" value={form.fastest_lap} onChange={e => setForm({...form, fastest_lap: e.target.value})} /><br />
        <button type="submit">Predict</button>
      </form>

      {result && (
        <div style={{ marginTop: '1rem' }}>
          <h3>Results:</h3>
          <p>🏁 Top 1 Chance: {(result.Top1_prob * 100).toFixed(2)}%</p>
          <p>🥉 Top 3 Chance: {(result.Top3_prob * 100).toFixed(2)}%</p>
          <p>🏅 Top 5 Chance: {(result.Top5_prob * 100).toFixed(2)}%</p>
          <p>📈 Predicted Position: {result.Predicted_Position.toFixed(2)}</p>
        </div>
      )}
    </div>
  );
}
