// frontend/src/components/Navbar.jsx
import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={{ background: "#eee", padding: "10px" }}>
      <Link to="/">Home</Link> |{" "}
      <Link to="/dashboard">Dashboard</Link> |{" "}
      <Link to="/tenants">Tenants</Link> |{" "}
      <Link to="/leases">Leases</Link> |{" "}
      <Link to="/login">Login</Link>
    </nav>
  );
}
