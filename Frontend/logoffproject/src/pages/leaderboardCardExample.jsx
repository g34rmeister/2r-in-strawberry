import React from "react";
import api from '../components/api'
import { useState } from 'react';
import LeaderboardCard from '../components/leaderboardCard.jsx'
import '../components/leaderboardCard.css'

function LeaderboardCardExample() {
    return (
        <div>
            <h1>HelloWorld</h1>
            <LeaderboardCard
                rank={1}
                name="donk"
                points={1000}
                avatarUrl="https://img-cdn.hltv.org/playerbodyshot/sEwjjWjn36V9aqH6i07aFx.png?ixlib=java-2.1.0&w=400&s=14a4ef10ad0fcd029d9b8872437a697e"
            />
            <LeaderboardCard
                rank={2}
                name="zywoo"
                points={697}
                avatarUrl="https://img-cdn.hltv.org/playerbodyshot/bxEhMYAhUwDXAO1gbuOwE7.png?ixlib=java-2.1.0&w=400&s=95005e4351561cb1427ae057fb2cbb25"
            />
            <LeaderboardCard
                rank={3}
                name="kyousuke"
                points={420}
                avatarUrl="https://img-cdn.hltv.org/playerbodyshot/_s6UUQ4E92xw1uSWWCafsK.png?ixlib=java-2.1.0&w=400&s=d94a122aa9a8ec89f0727656b69e2415"
            />
            <LeaderboardCard
                rank={4}
                name="coldzera"
                points={67}
                avatarUrl="https://img-cdn.hltv.org/playerbodyshot/eQN-pKLbiz_8oMSkAQVDfv.png?ixlib=java-2.1.0&w=400&s=23e87012c5ce9144ddda8e9dd8e69172"
            />
        </div>
    );
}

export default LeaderboardCardExample