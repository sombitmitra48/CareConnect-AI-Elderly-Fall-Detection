import React from 'react';
import './StatusCard.css';

const StatusCard = ({ status, lastCheck }) => {
  const formatTime = (date) => {
    return date.toLocaleString([], { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="status-card">
      <h2>System Status</h2>
      <div className={`status-indicator ${status}`}>
        <span className="status-dot"></span>
        <span>
          {status === 'active' ? 'Active & Monitoring' : 'Inactive'}
        </span>
      </div>
      <p>Last checked: <span>{formatTime(lastCheck)}</span></p>
    </div>
  );
};

export default StatusCard;