import { useState } from 'react'
import './App.css'
import { Routes, Route, Link } from 'react-router-dom';
import Login from "../src/pages/login"
import StartChallenge from './pages/start-challenge';
import LeaderboardCardExample from './pages/leaderboardCardExample';
import Challenges from './pages/challenges';
import History from './pages/history';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/start-challenge" element={<StartChallenge/>} />
        <Route path="/" element={<Login />} />
        <Route path="/leaderboardcardexample" element={<LeaderboardCardExample/>} />
        <Route path="/challenges" element={<Challenges/>} />
        <Route path="/history" element={<History/>} />
      </Routes>
    </>
  )
}

export default App
