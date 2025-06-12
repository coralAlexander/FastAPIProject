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
          navigate('/home');
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

  const showMessage = (text) => {
    setMessage(text);
    setTimeout(() => {
      setMessage('');
    }, 3000);
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-logo">C</div>
        <h2>Вход в аккаунт</h2>
        {message && <div className="notification">{message}</div>}
        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
          <div className="login-links">
            <a href="#">Забыли пароль?</a>
          </div>
          <button type="submit" className="submit-button">Войти</button>
        </form>
        <div className="register-link">
          Нет аккаунта? <a href="#">Регистрация</a>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
