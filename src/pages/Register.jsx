import React, { useState } from "react";
import axios from "axios";
import API_BASE_URL from "../config";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    if (!email || !password || !confirmPassword) {
      alert("⚠️ Please fill in all fields.");
      return;
    }

    if (password !== confirmPassword) {
      alert("❌ Passwords do not match.");
      return;
    }

    try {
      const res = await axios.post(`${API_BASE_URL}/register`, {
        email,
        password,
      });

      if (res.data.message === "Registration successful") {
        alert("✅ Registration successful! Please log in.");
        navigate("/login");
      } else {
        alert(res.data.error || "Registration failed. Try again.");
      }
    } catch (err) {
      console.error("Registration error:", err);
      if (err.response?.status === 400) {
        alert("⚠️ User already exists or invalid data.");
      } else {
        alert("⚠️ Network or server error. Please try again later.");
      }
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />
      <input
        type="password"
        placeholder="Enter your password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />
      <input
        type="password"
        placeholder="Confirm password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
      />
      <br />
      <button onClick={handleRegister}>Register</button>
    </div>
  );
}
