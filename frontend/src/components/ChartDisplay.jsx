import React from "react";
import CandlestickChart from "./CandlestickChart";

export default function ChartDisplay({ data }) {
  if (!data || !Array.isArray(data) || data.length === 0) return null;
  // Prepare all series and markers
  const candlestickData = data.map(row => ({
    time: row.Date,
    open: row.Open,
    high: row.High,
    low: row.Low,
    close: row.Close,
  }));
  const sma20Data = data.filter(row => row.SMA_20 !== undefined && row.SMA_20 !== null).map(row => ({
    time: row.Date,
    value: row.SMA_20
  }));
  const sma50Data = data.filter(row => row.SMA_50 !== undefined && row.SMA_50 !== null).map(row => ({
    time: row.Date,
    value: row.SMA_50
  }));
  // Markers for buy/sell signals
  const markers = data.filter(row => row.Signal).map(row => ({
    time: row.Date,
    position: row.Signal === 'buy' ? 'belowBar' : 'aboveBar',
    color: row.Signal === 'buy' ? '#26a69a' : '#ef5350',
    shape: row.Signal === 'buy' ? 'arrowUp' : 'arrowDown',
    text: row.Signal
  }));
  return (
    <div style={{ marginTop: 40, marginBottom: 40 }}>
      <CandlestickChart
        candlestickData={candlestickData}
        sma20Data={sma20Data}
        sma50Data={sma50Data}
        markers={markers}
      />
    </div>
  );
}
