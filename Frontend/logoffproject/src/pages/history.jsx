import React from "react";
import api from '../components/api'
import { useState } from 'react';
import LeaderboardCard from '../components/leaderboardCard.jsx'

function LeaderboardCardExample() {
    return (
        <div>
            <h1>HelloWorld</h1>
            <LeaderboardCard
                rank={1}
                name="John Doe"
                points={15000}
                avatarUrl="https://img-cdn.hltv.org/playerbodyshot/_s6UUQ4E92xw1uSWWCafsK.png?ixlib=java-2.1.0&w=400&s=d94a122aa9a8ec89f0727656b69e2415"
            />
        </div>
    );
}

export default LeaderboardCardExample