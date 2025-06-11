import React from 'react';
import {BrowserRouter as Router, Navigate, Route, Routes} from 'react-router-dom';
import LoginForm from './components/LoginForm';
import AddUserForm from './components/AddUserForm';
import Home from './components/HomeForm';
import UpdateUser from './components/UpdateUser';
import DeleteUser from './components/DeleteUser';
import UserInfo from './components/UserInfo';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate to="/login"/>}/>
                <Route path="/login" element={<LoginForm/>}/>
                <Route path="/home" element={<Home/>}/>
                <Route path="/adduser" element={<AddUserForm/>}/>
                <Route path="/updateuser" element={<UpdateUser/>}/>
                <Route path="/deleteuser" element={<DeleteUser/>}/>
                <Route path="/userinfo" element={<UserInfo/>}/>
            </Routes>
        </Router>
    );
};

export default App;
