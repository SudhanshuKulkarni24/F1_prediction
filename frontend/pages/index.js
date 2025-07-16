import { useEffect, useState } from 'react';

export default function Home() {
  const [form, setForm] = useState({ year: '', driver: '', race: '' });
  const [drivers, setDrivers] = useState([]);
  const [races, setRaces] = useState([]);
  const [result, setResult] = useState(null);
  const [loadingOptions, setLoadingOptions] = useState(false);

  const handleYearChange = (e) => {
    setForm({ ...form, year: e.target.value });
  };

  const handleLoadOptions = async () => {
    if (!form.year) return;
    setLoadingOptions(true);
    try {
      const res = await fetch(`/api/options?year=${form.year}`);
      const data = await res.json();
      setDrivers(data.drivers || []);
      setRaces(data.races || []);
    } catch (err) {
      console.error("Failed to load options", err);
    }
    setLoadingOptions(false);
  };

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
        <input
          type="text"
          name="year"
          value={form.year}
          onChange={handleYearChange}
          placeholder="e.g., 2023"
        />
        <button type="button" onClick={handleLoadOptions} style={{ marginLeft: 10 }}>
          🔄 Load Races & Drivers
        </button>
        <br /><br />

        {loadingOptions && <p>⏳ Loading races and drivers...</p>}

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
