// frontend/src/pages/Leases.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import API_BASE_URL from "../config";

export default function Leases() {
  const [leases, setLeases] = useState([]);
  const [form, setForm] = useState({
    unit_id: "",
    tenant_id: "",
    rent_amount: "",
    start_date: "",
    end_date: "",
  });

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/leases`)
      .then((r) => setLeases(r.data))
      .catch((e) => console.error(e));
  }, []);

  const handleSubmit = async () => {
    try {
      await axios.post(`${API_BASE_URL}/leases`, form);
      alert("Lease added!");
      const res = await axios.get(`${API_BASE_URL}/leases`);
      setLeases(res.data);
    } catch (e) {
      alert("Failed: " + (e.response?.data?.error || e.message));
    }
  };

  return (
    <div>
      <h2>Leases</h2>
      <div>
        <input
          placeholder="Unit ID"
          value={form.unit_id}
          onChange={(e) => setForm({ ...form, unit_id: e.target.value })}
        />
        <input
          placeholder="Tenant ID"
          value={form.tenant_id}
          onChange={(e) => setForm({ ...form, tenant_id: e.target.value })}
        />
        <input
          placeholder="Rent Amount"
          value={form.rent_amount}
          onChange={(e) => setForm({ ...form, rent_amount: e.target.value })}
        />
        <input
          type="date"
          placeholder="Start Date"
          value={form.start_date}
          onChange={(e) => setForm({ ...form, start_date: e.target.value })}
        />
        <input
          type="date"
          placeholder="End Date"
          value={form.end_date}
          onChange={(e) => setForm({ ...form, end_date: e.target.value })}
        />
        <button onClick={handleSubmit}>Add Lease</button>
      </div>
      <ul>
        {leases.map((l) => (
          <li key={l.id}>
            Lease #{l.id} — Unit {l.unit_id} — Tenant {l.tenant_id} — ₦{l.rent_amount}
          </li>
        ))}
      </ul>
    </div>
  );
}
