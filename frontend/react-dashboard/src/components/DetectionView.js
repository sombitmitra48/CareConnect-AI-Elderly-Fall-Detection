import React from 'react';
import './DetectionView.css';

const DetectionView = () => {
  return (
    <div className="detection-view">
      <h2>Live Detection</h2>
      <div className="video-container">
        <div className="video-placeholder">
          <p>Live Camera Feed</p>
          <div className="camera-icon">📷</div>
        </div>
      </div>
      <div className="detection-status">
        <p>No falls detected</p>
      </div>
    </div>
  );
};

export default DetectionView;