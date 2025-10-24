import React, { useState } from "react";
import axios from "axios";
import API_BASE_URL from "../config";
import { saveToken } from "../auth";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      // ✅ Corrected URL: no '/auth' prefix
      const res = await axios.post(`${API_BASE_URL}/login`, {
        email,
        password,
      });

      const token = res.data.token; // ✅ matches backend response key
      if (token) {
        saveToken(token);
        alert("✅ Login successful!");
        navigate("/dashboard");
      } else {
        alert("❌ Login failed — no token received.");
      }
    } catch (err) {
      console.error("Login error:", err);
      if (err.response?.status === 401) {
        alert("❌ Invalid credentials. Please check your email or password.");
      } else {
        alert("⚠️ Network or server error. Please try again later.");
      }
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />
      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
