import React, { useState, useEffect } from 'react';
import api from './api.jsx';

const leaderboardCard = () => {
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await api.get('userdata/global-leaderboard/');
        setLeaderboardData(response.data);
        setError(null);
      } catch (err) {
        console.error("Error fetching leaderboard:", err.response ? err.response.data : err.message);
        setError("Failed to load leaderboard data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  const getRankClass = (rank) => {
    if (rank <= 3) return `user-rank-item rank-${rank}`;
    return "user-rank-item";
  };

  if (loading) {
    return <div className="leaderboard-loading">Loading the Global Leaderboard...</div>;
  }

  if (error) {
    return <div className="leaderboard-error">{error}</div>;
  }

  if (leaderboardData.length === 0) {
    return <div className="leaderboard-empty">No leaderboard entries found.</div>;
  }

  return (
    <div className="leaderboard-container">
      <h2>🏆 Global Leaderboard</h2>
      <div className="leaderboard-list">
        {leaderboardData.map((entry, index) => (
          <div key={index} className={getRankClass(index + 1)}>
            {/* 1. Rank Circle */}
            <div className={`rank-circle ${index < 3 ? `rank-${index + 1}` : ''}`}>
              <span>{index + 1}</span>
            </div>

            {/* 2. User Info (Name & Points) */}
            <div className="user-info">
              <div className="user-name">{entry.username}</div>
              <div className="user-points">{entry.score} Points</div>
            </div>

            {/* 3. Avatar Image */}
            <img 
              src={`https://api.dicebear.com/7.x/initials/svg?seed=${entry.username}`}
              alt={`${entry.username}'s avatar`} 
              className="avatar" 
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default leaderboardCard;


