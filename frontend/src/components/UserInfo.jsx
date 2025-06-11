import React, { useState } from 'react';
import './UserInfo.css';

const UserInfo = () => {
  const [username, setUsername] = useState('');
  const [userInfo, setUserInfo] = useState(null);
  const [message, setMessage] = useState('');

  const handleGetInfo = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem('token');  // если используешь авторизацию

      const response = await fetch(`http://localhost:8000/users/username/${username}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`  // если нужен токен
        },
      });

      if (response.ok) {
        const data = await response.json();
        setUserInfo(data);
        setMessage('');
      } else {
        const errorData = await response.json();
        setUserInfo(null);
        setMessage(`❌ Error: ${errorData.detail}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setUserInfo(null);
      setMessage('❌ Error sending request');
    }
  };

  return (
    <div className="userinfo-container">
      <h2>Get User Info</h2>
      {message && <div className="notification">{message}</div>}
      <form onSubmit={handleGetInfo} className="userinfo-form">
        <div className="form-group">
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            placeholder="Enter username to search"
          />
        </div>
        <button type="submit" className="submit-button">Get Info</button>
      </form>

      {userInfo && (
        <div className="user-info">
          <h3>User Information:</h3>
          <p><strong>ID:</strong> {userInfo.id}</p>
          <p><strong>Username:</strong> {userInfo.username}</p>
          <p><strong>Email:</strong> {userInfo.email}</p>
          <p><strong>Role:</strong> {userInfo.role}</p>
        </div>
      )}
    </div>
  );
};

export default UserInfo;
