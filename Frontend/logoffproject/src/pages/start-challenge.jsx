import api from '../components/api'
import Droppable from '../components/droppable';
import { useState, useEffect } from 'react';
import Navbar from '../components/navbar';

function StartChallenge() {
    const [username, setUsername] = useState('');
    const [choice, setChoice] = useState('');
    
    useEffect(() => {
        api.get('/user/')
            .then(res => {setUsername(res.data.username)})
            .catch(err => {console.error('Failed to fetch user:', err)});
    }, []);

    const handleChange = (e) => setChoice(e.target.value);

    return(
        <>
            <h1>Hi {username || 'Guest'},</h1>
            <p>start a challenge?</p>
            <Droppable
                    label="Difficulty: "
                    options={[
                    { label: '★', value: 'easy' },
                    { label: '★★', value: 'mediumeasy' },
                    { label: '★★★', value: 'medium' },
                    { label: '★★★★', value: 'mediumhard' },
                    { label: '★★★★★', value: 'hard' },
                    ]}
                value={choice}
                onChange={handleChange}
            />

            <button>Start</button>
            <Navbar />
        </>
    );
}

export default StartChallenge;