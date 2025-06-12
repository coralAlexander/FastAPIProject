// src/components/FormLayout.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './FormLayout.css';  // стили общие для layout

const FormLayout = ({ title, children }) => {
  const navigate = useNavigate();

  const handleBackToHome = () => {
    navigate('/home');
  };

  return (
    <div className="form-page">
      <div className="form-header">
        <button onClick={handleBackToHome} className="back-button">← Back to Home</button>
      </div>
      <div className="form-container">
        <h2 className="form-title">{title}</h2>
        {children}
      </div>
    </div>
  );
};

export default FormLayout;
