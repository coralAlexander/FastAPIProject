import React, {useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import './HomeForm.css';

const Home = () => {
  const navigate = useNavigate();

  const handleNavigate = (path) => {
    navigate(path);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  return (
    <div className="home-container">
      <h1>Fast API Project - Home</h1>
      <div className="button-group">
        <button onClick={() => handleNavigate('/adduser')}>Create User</button>
        <button onClick={() => handleNavigate('/updateuser')}>Update User</button>
        <button onClick={() => handleNavigate('/deleteuser')}>Delete User</button>
        <button onClick={() => handleNavigate('/userinfo')}>Get User Info</button>
        <button onClick={handleLogout} className="logout-button">Sign out</button>
      </div>
    </div>
  );
};

export default Home;
