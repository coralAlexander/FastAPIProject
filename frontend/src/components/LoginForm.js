import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginForm.css';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        showMessage('✅ Login successful! Redirecting...');
        setTimeout(() => {
          navigate('/home');  // редирект через 1.5 сек
        }, 1500);
      } else {
        const errorData = await response.json();
        showMessage(`❌ Login failed: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Error:', error);
      showMessage('❌ Error sending request');
    }
  };

  // Показ сообщения + auto hide через 3 сек
  const showMessage = (text) => {
    setMessage(text);
    setTimeout(() => {
      setMessage('');
    }, 3000);
  };

  return (
    <div className="login-container">
      <div className="page-header">Fast API Project</div>  {/* Заголовок */}
      {message && <div className="notification">{message}</div>}
      <form onSubmit={handleLogin} className="login-form">
        <h2>Login</h2>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
            placeholder="Enter username"
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            placeholder="Enter password"
          />
        </div>
        <button type="submit" className="submit-button">Login</button>
      </form>
    </div>
  );
};

export default LoginForm;
