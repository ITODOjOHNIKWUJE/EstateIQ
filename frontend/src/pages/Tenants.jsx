// frontend/src/pages/Tenants.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import API_BASE_URL from "../config";

export default function Tenants() {
  const [tenants, setTenants] = useState([]);
  const [form, setForm] = useState({ name: "", email: "", phone: "" });

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/tenants`)
      .then((r) => setTenants(r.data))
      .catch((e) => console.error(e));
  }, []);

  const handleSubmit = async () => {
    try {
      await axios.post(`${API_BASE_URL}/tenants`, form);
      alert("Tenant added!");
      setForm({ name: "", email: "", phone: "" });
      const res = await axios.get(`${API_BASE_URL}/tenants`);
      setTenants(res.data);
    } catch (e) {
      alert("Failed to add tenant: " + (e.response?.data?.error || e.message));
    }
  };

  return (
    <div>
      <h2>Tenants</h2>
      <div>
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <input
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          placeholder="Phone"
          value={form.phone}
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
        />
        <button onClick={handleSubmit}>Add Tenant</button>
      </div>
      <ul>
        {tenants.map((t) => (
          <li key={t.id}>
            {t.name} — {t.email} — {t.phone || "N/A"}
          </li>
        ))}
      </ul>
    </div>
  );
}
