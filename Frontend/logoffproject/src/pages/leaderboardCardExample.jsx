import React from "react";
import api from '../components/api'
import { useState } from 'react';
import LeaderboardCard from '../components/leaderboardCard.jsx'
import '../components/leaderboardCard.css'

function LeaderboardCardExample() {
    return (
        <div>
            <h1>HelloWorld</h1>
            <LeaderboardCard/>

        </div>
    );
}

export default LeaderboardCardExample