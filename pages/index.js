import { useState } from 'react';

export default function Home() {
    const [driver, setDriver] = useState('');
    const [avgLapTime, setAvgLapTime] = useState('');
    const [fastestLap, setFastestLap] = useState('');
    const [result, setResult] = useState(null);

    const predict = async () => {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ driver, avg_lap_time: parseFloat(avgLapTime), fastest_lap: parseFloat(fastestLap) })
        });
        const data = await res.json();
        setResult(data);
    };

    return (
        <div>
            <h1>🏁 F1 Finish Prediction</h1>
            <input value={driver} onChange={e => setDriver(e.target.value)} placeholder="Driver name" />
            <input value={avgLapTime} onChange={e => setAvgLapTime(e.target.value)} placeholder="Avg Lap Time" />
            <input value={fastestLap} onChange={e => setFastestLap(e.target.value)} placeholder="Fastest Lap" />
            <button onClick={predict}>Predict</button>
            {result && (
                <div>
                    <h2>Prediction</h2>
                    <p>Top 1 %: {(result.Top1_prob * 100).toFixed(2)}%</p>
                    <p>Top 3 %: {(result.Top3_prob * 100).toFixed(2)}%</p>
                    <p>Top 5 %: {(result.Top5_prob * 100).toFixed(2)}%</p>
                    <p>Predicted Final Position: {result.FinalPos}</p>
                </div>
            )}
        </div>
    );
}