import React, { useState, useEffect } from 'react';
import StatusCard from './StatusCard';
import DetectionView from './DetectionView';
import AlertsSection from './AlertsSection';
import EmergencySection from './EmergencySection';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  const [systemStatus, setSystemStatus] = useState('active');
  const [lastCheck, setLastCheck] = useState(new Date());
  const [alerts, setAlerts] = useState([
    {
      id: 1,
      time: 'Today, 10:30 AM',
      status: 'resolved',
      message: 'Fall detected in living room. Volunteer response time: 2 minutes.'
    },
    {
      id: 2,
      time: 'Yesterday, 3:45 PM',
      status: 'resolved',
      message: 'Manual alert triggered. Caregiver notified.'
    }
  ]);

  useEffect(() => {
    // Simulate periodic status updates
    const interval = setInterval(() => {
      setLastCheck(new Date());
    }, 60000);

    return () => clearInterval(interval);
  }, []);

  const handleEmergencyCall = () => {
    if (window.confirm('Are you sure you want to trigger an emergency alert?')) {
      const newAlert = {
        id: alerts.length + 1,
        time: 'Just now',
        status: 'pending',
        message: 'Manual emergency alert triggered'
      };
      
      setAlerts(prev => [newAlert, ...prev]);
      alert('Emergency alert has been sent! Help is on the way.');
    }
  };

  return (
    <div className="dashboard">
      <StatusCard status={systemStatus} lastCheck={lastCheck} />
      <DetectionView />
      <AlertsSection alerts={alerts} />
      <EmergencySection onEmergencyCall={handleEmergencyCall} />
    </div>
  );
};

export default Dashboard;