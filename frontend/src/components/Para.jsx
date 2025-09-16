
import React, { useState } from "react";
import '../form.css';
import ChartDisplay from './ChartDisplay';

export default function SearchForm() {
  const [formData, setFormData] = useState({
    symbol: "",
    start: "",
    end: "",
    interval: "",
    marketType: ""
  });
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
  setChartData(null);
    try {
      const params = new URLSearchParams({
        symbol: formData.symbol,
        interval: formData.interval,
        market_type: formData.marketType,
      });
      if (formData.start) params.append('start', formData.start);
      if (formData.end) params.append('end', formData.end);
      const res = await fetch(`http://127.0.0.1:5000/data?${params.toString()}`);
      if (!res.ok) throw new Error('Failed to fetch data');
      const data = await res.json();
  setChartData(data);
    } catch (err) {
      setError('Could not load data.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <form className="search-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          <input
            type="text"
            name="symbol"
            placeholder="ORCL"
            value={formData.symbol}
            onChange={handleChange}
          />
          <input
            type="date"
            name="start"
            value={formData.start}
            onChange={handleChange}
          />
          <input
            type="date"
            name="end"
            value={formData.end}
            onChange={handleChange}
          />
          <select
            name="interval"
            value={formData.interval}
            onChange={handleChange}
          >
            <option value="">Select Interval</option>
            <option value="1m">1 Minute</option>
            <option value="5m">5 Minutes</option>
            <option value="15m">15 minutes</option>
            <option value="1d">1 Day</option>
          </select>
          <select
            name="marketType"
            value={formData.marketType}
            onChange={handleChange}
          >
            <option value="">Select Market Type</option>
            <option value="stock">Stock</option>
            <option value="crypto">Crypto</option>
            <option value="forex">Forex</option>
          </select>
        </div>
        <button type="submit" className="search-btn">Search</button>
      </form>
      {loading && <div style={{ color: '#fff', marginTop: '1rem' }}>Loading...</div>}
      {error && <div style={{ color: 'red', marginTop: '1rem' }}>{error}</div>}
      {chartData && <ChartDisplay data={chartData} />}
    </>
  );
}