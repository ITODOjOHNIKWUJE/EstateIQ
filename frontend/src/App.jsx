// frontend/src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SidebarLayout from "./components/SidebarLayout";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Tenants from "./pages/Tenants";
import Leases from "./pages/Leases";
import Properties from "./pages/Properties";
import Login from "./pages/Login";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<SidebarLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/tenants" element={<Tenants />} />
          <Route path="/leases" element={<Leases />} />
          <Route path="/properties" element={<Properties />} />
        </Route>
      </Routes>
    </Router>
  );
}
