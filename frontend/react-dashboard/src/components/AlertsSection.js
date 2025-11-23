import React from 'react';
import './AlertsSection.css';

const AlertsSection = ({ alerts }) => {
  return (
    <div className="alerts-section">
      <h2>Recent Alerts</h2>
      <div className="alert-list">
        {alerts.map(alert => (
          <div key={alert.id} className="alert-item">
            <div className="alert-header">
              <span className="alert-time">{alert.time}</span>
              <span className={`alert-status ${alert.status}`}>
                {alert.status.charAt(0).toUpperCase() + alert.status.slice(1)}
              </span>
            </div>
            <p>{alert.message}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertsSection;