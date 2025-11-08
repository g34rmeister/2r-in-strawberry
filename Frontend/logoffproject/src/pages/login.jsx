import React from "react";
import api from '../components/api'
import { useState } from 'react';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [user, setUser] = useState(null);

    const onSubmit = (event) => {
        event.preventDefault();//Prevent normal submit
        setError(null);

        api.post('/login/', {
            username: username,
            password: password,
        })
        .then(result => {
            //login success
            console.log("LOGIN SUCCESS!");
            setUser(result.data);
        })
        .catch(error => {
            //login failure
            console.error('Login failed: ', error);
            if (error.response) {
                setError(error.response.data.error || 'Login failed');
            } else {
                setError('Unkown error')
            }
        })
    }

    return (
        <form onSubmit={onSubmit}>
            <h2>Login</h2>
            <div>
                <label>Username:</label>
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
            </div>
            <div>
                <label>Password:</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
            <button type="submit">Login</button>
        </form>
    )
}

export default Login