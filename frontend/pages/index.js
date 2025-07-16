import { useEffect, useState } from 'react';

export default function Home() {
  const [form, setForm] = useState({ year: '', driver: '', race: '' });
  const [drivers, setDrivers] = useState([]);
  const [races, setRaces] = useState([]);
  const [result, setResult] = useState(null);

  useEffect(() => {
    if (form.year) {
      fetch(`/api/options?year=${form.year}`)
        .then(res => res.json())
        .then(data => {
          setDrivers(data.drivers || []);
          setRaces(data.races || []);
        });
    }
  }, [form.year]);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
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
    <main style={{ padding: 20, fontFamily: 'Arial' }}>
      <h1>🏎️ F1 Finish Predictor</h1>

      <form onSubmit={handleSubmit}>
        <label>Year:</label>
        <input type="text" name="year" value={form.year} onChange={handleChange} placeholder="e.g., 2023" /><br /><br />

        <label>Driver:</label>
        <select name="driver" value={form.driver} onChange={handleChange}>
          <option value="">Select Driver</option>
          {drivers.map(d => <option key={d}>{d}</option>)}
        </select><br /><br />

        <label>Race:</label>
        <select name="race" value={form.race} onChange={handleChange}>
          <option value="">Select Race</option>
          {races.map(r => <option key={r}>{r}</option>)}
        </select><br /><br />

        <button type="submit">🔮 Predict</button>
      </form>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h2>📊 Prediction:</h2>
          <p><strong>Driver:</strong> {result.driver}</p>
          <p><strong>Race:</strong> {result.race}</p>
          <p><strong>Year:</strong> {result.year}</p>
          <p><strong>Top 1 Finish Probability:</strong> {result.Top1}</p>
          <p><strong>Top 3 Finish Probability:</strong> {result.Top3}</p>
          <p><strong>Top 5 Finish Probability:</strong> {result.Top5}</p>
        </div>
      )}
    </main>
  );
}
