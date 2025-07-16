import { useState } from "react";

export default function Home() {
  const [form, setForm] = useState({ driver: "", avg_lap_time: "", fastest_lap: "" });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          driver: form.driver,
          avg_lap_time: parseFloat(form.avg_lap_time),
          fastest_lap: parseFloat(form.fastest_lap),
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Prediction failed");
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "2rem", maxWidth: 400, margin: "0 auto" }}>
      <h1>🏁 F1 Race Prediction</h1>
      <form onSubmit={onSubmit}>
        <input placeholder="Driver name" value={form.driver} onChange={(e) => setForm({ ...form, driver: e.target.value })} /><br /><br />
        <input placeholder="Avg Lap Time" type="number" step="any" value={form.avg_lap_time} onChange={(e) => setForm({ ...form, avg_lap_time: e.target.value })} /><br /><br />
        <input placeholder="Fastest Lap Time" type="number" step="any" value={form.fastest_lap} onChange={(e) => setForm({ ...form, fastest_lap: e.target.value })} /><br /><br />
        <button type="submit">Predict</button>
      </form>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {result && (
        <div style={{ marginTop: "1.5rem" }}>
          <h2>Prediction Results</h2>
          <p>🏆 Probability of Winning (Top 1): {(result.top1_prob * 100).toFixed(2)}%</p>
          <p>🥉 Probability Top 3: {(result.top3_prob * 100).toFixed(2)}%</p>
          <p>🏅 Probability Top 5: {(result.top5_prob * 100).toFixed(2)}%</p>
          {result.predicted_position !== undefined && (
            <p>📈 Predicted Position: {result.predicted_position.toFixed(2)}</p>
          )}
        </div>
      )}
    </div>
  );
}
