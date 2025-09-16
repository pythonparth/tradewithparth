import { useState } from 'react'
import Background from './components/bg'
import Para from './components/Para'
import './App.css'

function App() {
  

  return (
    <>
      <Background />
      <div style={{ position: 'relative', zIndex: 1 }}>
        <h1 style={{ textAlign: 'center', fontSize: '3rem', fontWeight: 'bold', fontStyle: 'italic',marginTop: '2rem', marginBottom: '1.5rem', letterSpacing: '1px', paddingBottom: 80, textShadow: '2px 2px 8px rgba(0, 0, 0, 0.4), 0 0 15px rgba(255, 215, 0, 0.6)'
 }}>💸💸$AWARIYA $ETH $TOCKS💸💸</h1>
      </div>
      <Para />
    </>
  )
}

export default App
