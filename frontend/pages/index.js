import { useState, useEffect } from "react";

export default function Home() {
  const [form, setForm] = useState({
    year: "",
    race: "",
    driver: ""
  });

  const [drivers, setDrivers] = useState([]);
  const [races, setRaces] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (form.year) {
      fetch(`/api/options?year=${form.year}`)
        .then((res) => res.json())
        .then((data) => {
          setRaces(data.races || []);
          setDrivers(data.drivers || []);
        })
        .catch((err) => console.error("Error fetching options:", err));
    }
  }, [form.year]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Prediction error:", err);
      setResult({ error: "Failed to predict" });
    }
    setLoading(false);
  };

  return (
    <main style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>🏎️ F1 Race Outcome Predictor</h1>
      <form onSubmit={handleSubmit}>
        <label>Year:</label><br />
        <input
          type="text"
          placeholder="e.g. 2024"
          value={form.year}
          onChange={(e) => setForm({ ...form, year: e.target.value })}
        />
        <br /><br />

        <label>Race Name:</label><br />
        <select
          value={form.race}
          onChange={(e) => setForm({ ...form, race: e.target.value })}
        >
          <option value="">--Select Race--</option>
          {races.map((r) => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>
        <br /><br />

        <label>Driver:</label><br />
        <select
          value={form.driver}
          onChange={(e) => setForm({ ...form, driver: e.target.value })}
        >
          <option value="">--Select Driver--</option>
          {drivers.map((d) => (
            <option key={d} value={d}>{d}</option>
          ))}
        </select>
        <br /><br />

        <button type="submit" disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h3>📊 Prediction Results:</h3>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <ul>
              <li><strong>Top 1 Probability:</strong> {(result.top1 * 100).toFixed(2)}%</li>
              <li><strong>Top 3 Probability:</strong> {(result.top3 * 100).toFixed(2)}%</li>
              <li><strong>Top 5 Probability:</strong> {(result.top5 * 100).toFixed(2)}%</li>
            </ul>
          )}
        </div>
      )}
    </main>
  );
}
