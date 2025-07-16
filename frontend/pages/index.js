import { useState, useEffect } from "react";

export default function Home() {
  const [years, setYears] = useState([]);
  const [races, setRaces] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [form, setForm] = useState({ year: "", race: "", driver: "" });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  // Fetch options on load
  useEffect(() => {
    fetch("/api/options")
      .then((r) => r.json())
      .then((data) => {
        setYears(data.years);
        setDrivers(data.drivers);
      })
      .catch(() => { /* ignore */ });
  }, []);

  // When year changes, load races for that year
  useEffect(() => {
    if (form.year) {
      fetch(`/api/options?year=${form.year}`)
        .then((r) => r.json())
        .then((data) => setRaces(data.races))
        .catch(() => { /* ignore */ });
    }
  }, [form.year]);

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Prediction failed");
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif", maxWidth: 400, margin: "auto" }}>
      <h1>🏎️ F1 Race Predictor</h1>
      <form onSubmit={onSubmit}>
        <label>Year: </label>
        <select value={form.year} onChange={(e) => setForm({ ...form, year: e.target.value })}>
          <option value="">--Select Year--</option>
          {years.map((y) => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>
        <br /><br />

        <label>Race: </label>
        <select value={form.race} onChange={(e) => setForm({ ...form, race: e.target.value })}>
          <option value="">--Select Race--</option>
          {races.map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
        <br /><br />

        <label>Driver: </label>
        <select value={form.driver} onChange={(e) => setForm({ ...form, driver: e.target.value })}>
          <option value="">--Select Driver--</option>
          {drivers.map((d) => (
            <option key={d} value={d}>{d}</option>
          ))}
        </select>
        <br /><br />

        <button type="submit">Predict</button>
      </form>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Prediction Results</h2>
          <p>Top 1 Chance: {(result.top1_prob * 100).toFixed(2)}%</p>
          <p>Top 3 Chance: {(result.top3_prob * 100).toFixed(2)}%</p>
          <p>Top 5 Chance: {(result.top5_prob * 100).toFixed(2)}%</p>
          {result.predicted_position !== undefined && (
            <p>Predicted Position: {result.predicted_position.toFixed(1)}</p>
          )}
        </div>
      )}
    </div>
  );
}
