import api from '../components/api'
import Droppable from '../components/droppable';
import { useState, useEffect } from 'react';
import Navbar from '../components/navbar';
import React from 'react';
import { useNavigate } from 'react-router-dom';


function StartChallenge() {
    const [choice, setChoice] = useState('easy');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleStart = async () => {
        setError(null);

        try {
            await api.post('plantnet/getrandomplant/', {
                difficulty: choice
            });

            navigate('/challenges')
        } catch (err) {
            console.error("Error starting challenge:", err);
            setError("Failed to start challenge. Please try again.");
        }
    }

    //<h2>Welcome, {username || 'Guest'}!</h2>

    const handleChange = (e) => setChoice(e.target.value);
    return(
        <>
            <h2>Welcome, User!</h2>
            <p>Start a challenge?</p>
            <Droppable
                label="Difficulty"
                options={[
                    { label: '★', value: 'easy' },
                    { label: '★★', value: 'mid' },
                    { label: '★★★', value: 'hard' }
                ]}
                value={choice}
                onChange={handleChange}
            />

            <button onClick={handleStart}>Start</button>
            <Navbar />
        </>
    );
}

export default StartChallenge;