import { useState} from "react";

import React from 'react';

const leaderboardCard = ({ rank, name, points, avatarUrl }) => {
  const getRankClass = (rank) => {
    if (rank <= 3) return `user-rank-item rank-${rank}`;
    return "user-rank-item";
  };

  return (
    <div className={getRankClass(rank)}>
    {/* 1. Rank Circle */}
      <div className={`rank-circle ${rank <= 3 ? `rank-${rank}` : ''}`}>
        <span>{rank}</span>
      </div>

    {/* 2. User Info (Name & Points) */}
      <div className="user-info">
        <div className="user-name">{name}</div>
        <div className="user-points">{points} Points</div>
      </div>

    {/* 3. Avatar Image */}
      <img src={avatarUrl} alt={`${name}'s avatar`} className="avatar" />
    </div>
  );
};

export default leaderboardCard;