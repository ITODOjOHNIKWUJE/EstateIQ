// frontend/src/pages/Login.jsx
import React, { useState } from 'react';
import axios from 'axios';
import API_BASE_URL from '../config';
import { saveToken } from '../auth';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post(`${API_BASE_URL}/api/auth/login`, { email, password });
      const token = res.data.access_token;
      if (token) {
        saveToken(token);
        alert('Login successful');
        navigate('/dashboard');
      } else {
        alert('Login failed');
      }
    } catch (e) {
      console.error(e);
      alert('Login failed: ' + (e.response?.data?.error || e.message));
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        placeholder='Email'
        value={email}
        onChange={e => setEmail(e.target.value)}
      /><br />
      <input
        placeholder='Password'
        type='password'
        value={password}
        onChange={e => setPassword(e.target.value)}
      /><br />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
