import React from "react";
import api from '../components/api'
import { useState } from 'react';
import LeaderboardCard from '../components/leaderboardCard.jsx'
import '../components/leaderboardCard.css'
import Navbar from '../components/navbar';

function LeaderboardCardExample() {

    return (
        <>
        <div>
            <h1></h1>
            <LeaderboardCard/>

        </div>
        <Navbar />
        </>
    );
}

export default LeaderboardCardExample