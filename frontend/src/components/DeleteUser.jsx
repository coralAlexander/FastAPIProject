import React, { useState } from 'react';
import './DeleteUser.css';

const DeleteUser = () => {
  const [username, setUsername] = useState('');
  const [message, setMessage] = useState('');

  const handleDelete = async (e) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem('token');  // если ты используешь авторизацию

      const response = await fetch(`http://localhost:8000/users/remove/${username}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`  // если нужен токен
        },
      });

      if (response.ok) {
        const data = await response.json();
        showMessage(`✅ User deleted! ${data.detail}`);
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
    <div className="delete-container">
      <h2>Delete User</h2>
      {message && <div className="notification">{message}</div>}
      <form onSubmit={handleDelete} className="delete-form">
        <div className="form-group">
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            placeholder="Enter username to delete"
          />
        </div>
        <button type="submit" className="submit-button">Delete User</button>
      </form>
    </div>
  );
};

export default DeleteUser;
