import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Routes, Route, Link } from 'react-router-dom';
import Login from "../src/pages/login"
import LeaderboardCardExample from './pages/leaderboardCardExample';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/leaderboardcardexample" element={<LeaderboardCardExample/>} />
      </Routes>
    </>
  )
}

export default App
