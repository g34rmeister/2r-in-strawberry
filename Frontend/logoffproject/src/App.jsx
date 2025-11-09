import { useState } from 'react'
import './App.css'
import { Routes, Route, Link } from 'react-router-dom';
import Login from "../src/pages/login"
import Challenges from './pages/challenges';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Routes>
        <Route path="/login" element={<Login/>} />
        <Route path="/challenges" element={<Challenges/>} />
      </Routes>
    </>
  )
}

export default App
