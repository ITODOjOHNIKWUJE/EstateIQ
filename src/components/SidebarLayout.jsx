// frontend/src/components/SidebarLayout.jsx
import React from "react";
import { Link, Outlet } from "react-router-dom";

export default function SidebarLayout() {
  const menuItems = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Properties", path: "/properties" },
    { name: "Tenants", path: "/tenants" },
    { name: "Leases", path: "/leases" },
    { name: "Payments", path: "/dashboard" }, // same data as before for now
  ];

  return (
    <div style={{ display: "flex", minHeight: "100vh", backgroundColor: "#f5f6fa" }}>
      {/* Sidebar */}
      <div
        style={{
          width: "240px",
          backgroundColor: "#1E293B",
          color: "white",
          padding: "20px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <h2 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "30px" }}>
          EstateIQ
        </h2>
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            style={{
              color: "white",
              textDecoration: "none",
              padding: "10px 0",
              marginBottom: "10px",
              borderRadius: "6px",
            }}
            onMouseOver={(e) => (e.target.style.background = "#334155")}
            onMouseOut={(e) => (e.target.style.background = "transparent")}
          >
            {item.name}
          </Link>
        ))}
      </div>

      {/* Main content */}
      <div style={{ flex: 1, padding: "30px" }}>
        <Outlet />
      </div>
    </div>
  );
}
