import React from 'react';
import './EmergencySection.css';

const EmergencySection = ({ onEmergencyCall }) => {
  const teamMembers = [
    {
      id: 1,
      name: "Dr. Sarah Johnson",
      role: "General Practitioner",
      distance: "0.8 km away",
      icon: "👨‍⚕️"
    },
    {
      id: 2,
      name: "Mary Wilson",
      role: "Volunteer",
      distance: "0.3 km away",
      icon: "👩‍🦰"
    }
  ];

  return (
    <div className="emergency-section">
      <h2>Emergency Response</h2>
      <div className="response-team">
        {teamMembers.map(member => (
          <div key={member.id} className="team-member">
            <div className="member-icon">{member.icon}</div>
            <div className="member-info">
              <h3>{member.name}</h3>
              <p>{member.role}</p>
              <p className="distance">{member.distance}</p>
            </div>
          </div>
        ))}
      </div>
      <button className="emergency-button" onClick={onEmergencyCall}>
        🚨 Emergency Call
      </button>
    </div>
  );
};

export default EmergencySection;