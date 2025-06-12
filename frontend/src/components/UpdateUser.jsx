import React, { useState } from 'react';
import FormLayout from './FormLayout';  // ✅ добавляем FormLayout
import './UpdateUser.css';  // можешь оставить для своих form-group, если есть

const UpdateUser = () => {
  const [userId, setUserId] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('user');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const updateData = {
      username: username || undefined,
      email: email || undefined,
      password: password || undefined,
      role: role || undefined,
    };

    try {
      const token = localStorage.getItem('token');

      const response = await fetch(`http://localhost:8000/users/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updateData)
      });

      if (response.ok) {
        const data = await response.json();
        showMessage(`✅ User updated! ID: ${data.id}`);
      } else {
        const errorData = await response.json();
        showMessage(`❌ Error: ${errorData.detail}`);
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
    <FormLayout title="Update User">  {/* ✅ теперь общий красивый layout */}
      {message && <div className="notification">{message}</div>}
      <form onSubmit={handleSubmit} className="user-form">  {/* user-form можно оставить вместо update-form */}
        <div className="form-group">
          <label>User ID:</label>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            required
            placeholder="Enter User ID"
          />
        </div>
        <div className="form-group">
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter new username"
          />
        </div>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter new email"
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter new password"
          />
        </div>
        <div className="form-group">
          <label>Role:</label>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <button type="submit" className="submit-button">Update User</button>
      </form>
    </FormLayout>
  );
};

export default UpdateUser;
