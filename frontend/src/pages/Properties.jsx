// frontend/src/pages/Properties.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import API_BASE_URL from "../config";

export default function Properties() {
  const [properties, setProperties] = useState([]);
  const [form, setForm] = useState({ name: "", location: "", type: "" });

  const loadProperties = () => {
    axios
      .get(`${API_BASE_URL}/properties`)
      .then((r) => setProperties(r.data))
      .catch((e) => console.error(e));
  };

  useEffect(() => {
    loadProperties();
  }, []);

  const handleSubmit = async () => {
    try {
      await axios.post(`${API_BASE_URL}/properties`, form);
      alert("Property added!");
      setForm({ name: "", location: "", type: "" });
      loadProperties();
    } catch (e) {
      alert("Error adding property: " + (e.response?.data?.error || e.message));
    }
  };

  return (
    <div>
      <h2 style={{ marginBottom: "20px" }}>Properties</h2>
      <div
        style={{
          background: "white",
          padding: "20px",
          borderRadius: "8px",
          boxShadow: "0 1px 4px rgba(0,0,0,0.1)",
          marginBottom: "30px",
        }}
      >
        <h3>Add New Property</h3>
        <div style={{ display: "flex", gap: "10px", marginTop: "10px" }}>
          <input
            placeholder="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
          <input
            placeholder="Location"
            value={form.location}
            onChange={(e) => setForm({ ...form, location: e.target.value })}
          />
          <input
            placeholder="Type"
            value={form.type}
            onChange={(e) => setForm({ ...form, type: e.target.value })}
          />
          <button onClick={handleSubmit}>Add Property</button>
        </div>
      </div>

      <div
        style={{
          background: "white",
          padding: "20px",
          borderRadius: "8px",
          boxShadow: "0 1px 4px rgba(0,0,0,0.1)",
        }}
      >
        <h3>All Properties</h3>
        <ul>
          {properties.map((p) => (
            <li key={p.id}>
              <strong>{p.name}</strong> — {p.location} ({p.type})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
