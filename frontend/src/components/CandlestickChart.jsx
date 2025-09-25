import React, { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

/**
 * CandlestickChart component
 * @param {Object[]} candlestickData - Array of candlestick objects: { time, open, high, low, close }
 * @param {Object[]} sma20Data - Array of SMA 20 points: { time, value }
 * @param {Object[]} sma50Data - Array of SMA 50 points: { time, value }
 * @param {Object[]} markers - Array of marker objects for buy/sell signals
 */
export default function CandlestickChart({ candlestickData, sma20Data, sma50Data, markers }) {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!candlestickData || !Array.isArray(candlestickData) || candlestickData.length === 0) return;
    if (!chartContainerRef.current) return;

    // Clean up previous chart
    if (chartRef.current) {
      chartRef.current.remove();
      chartRef.current = null;
    }

    chartRef.current = createChart(chartContainerRef.current, {
      layout: {
        background: { color: '#18191A' },
        textColor: '#fff',
      },
      width: chartContainerRef.current.clientWidth,
      height: 400,
      grid: {
        vertLines: { color: '#444' },
        horzLines: { color: '#444' },
      },
    });

    const candleSeries = chartRef.current.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderDownColor: '#ef5350',
      borderUpColor: '#26a69a',
      wickDownColor: '#ef5350',
      wickUpColor: '#26a69a',
    });
    candleSeries.setData(candlestickData);
    if (markers && markers.length > 0) {
      candleSeries.setMarkers(markers);
    }

    // Add SMA 20 line
    if (sma20Data && sma20Data.length > 0) {
      const sma20Series = chartRef.current.addLineSeries({ color: '#2962FF', lineWidth: 2, title: 'SMA 20' });
      sma20Series.setData(sma20Data);
    }
    // Add SMA 50 line
    if (sma50Data && sma50Data.length > 0) {
      const sma50Series = chartRef.current.addLineSeries({ color: '#FF6D00', lineWidth: 2, title: 'SMA 50' });
      sma50Series.setData(sma50Data);
    }
    
    chartRef.current.timeScale().fitContent();

    // Responsive resize
    const handleResize = () => {
      if (chartRef.current && chartContainerRef.current) {
        chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [candlestickData, sma20Data, sma50Data, markers]);

  return (
    <div ref={chartContainerRef} style={{ width: '100%', height: 400, background: '#18191A', borderRadius: 8, boxShadow: '0 2px 12px #0004' }} />
  );
}
