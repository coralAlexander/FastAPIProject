import React, { useState } from 'react';
import FormLayout from './FormLayout';  // ✅ импортируем layout
import './AddUserForm.css';  // можно оставить для своих form-group и т.п.

const AddUserForm = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('user');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = {
      username,
      email,
      password,
      role
    };

    try {
      const response = await fetch('http://localhost:8000/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(userData)
      });

      if (response.ok) {
        const data = await response.json();
        showMessage(`✅ User created! ID: ${data.id}`);
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
    <FormLayout title="Add User">  {/* ✅ используем общий layout */}
      {message && <div className="notification">{message}</div>}
      <form onSubmit={handleSubmit} className="user-form">
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
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            placeholder="Enter email"
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
        <div className="form-group">
          <label>Role</label>
          <select value={role} onChange={e => setRole(e.target.value)}>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <button type="submit" className="submit-button">Add User</button>
      </form>
    </FormLayout>
  );
};

export default AddUserForm;
