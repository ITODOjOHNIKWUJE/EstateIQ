// frontend/src/pages/Dashboard.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";
import API_BASE_URL from "../config";
import { getToken, removeToken } from "../auth";
import { useNavigate } from "react-router-dom";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, CartesianGrid
} from "recharts";

export default function Dashboard() {
  const [overview, setOverview] = useState(null);
  const [incomeHistory, setIncomeHistory] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = getToken();
    if (!token) { navigate("/login"); return; }

    // fetch overview (no token required if you prefer; we use token for protected APIs)
    axios.get(`${API_BASE_URL}/stats/overview`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => setOverview(r.data))
      .catch(e => {
        console.error(e);
        if (e.response && e.response.status === 401) { removeToken(); navigate("/login"); }
      });

    axios.get(`${API_BASE_URL}/stats/income_by_months`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => setIncomeHistory(r.data))
      .catch(e => console.error(e));
  }, [navigate]);

  if (!overview) {
    return <div>Loading analytics...</div>;
  }

  const cards = [
    { title: "Properties", value: overview.total_properties },
    { title: "Tenants", value: overview.total_tenants },
    { title: "Active Leases", value: overview.total_leases },
    { title: "Monthly Income (₦)", value: overview.monthly_income }
  ];

  return (
    <div>
      <h1 style={{ marginBottom: 16 }}>Analytics Overview</h1>

      <div style={{ display: "flex", gap: 16, marginBottom: 24 }}>
        {cards.map(c => (
          <div key={c.title} style={{ background: "white", padding: 20, borderRadius: 8, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", minWidth: 180 }}>
            <div style={{ fontSize: 12, color: "#666" }}>{c.title}</div>
            <div style={{ fontSize: 22, fontWeight: 700, marginTop: 8 }}>{c.value}</div>
          </div>
        ))}
        <div style={{ background: "white", padding: 20, borderRadius: 8, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", minWidth: 200 }}>
          <div style={{ fontSize: 12, color: "#666" }}>Occupancy Rate</div>
          <div style={{ fontSize: 22, fontWeight: 700, marginTop: 8 }}>{overview.occupancy_rate}%</div>
        </div>
      </div>

      <div style={{ display: "flex", gap: 16 }}>
        <div style={{ background: "white", padding: 20, borderRadius: 8, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", flex: 1 }}>
          <h3>Income - Last 12 Months</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={incomeHistory}>
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="total" stroke="#2563eb" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={{ background: "white", padding: 20, borderRadius: 8, boxShadow: "0 1px 4px rgba(0,0,0,0.08)", width: 380 }}>
          <h3>Payments (quick view)</h3>
          <div style={{ maxHeight: 250, overflowY: "auto" }}>
            {/* quick list of latest payments */}
            <LatestPayments />
          </div>
        </div>
      </div>
    </div>
  );
}

// small helper component to show latest payments (keeps file self-contained)
function LatestPayments() {
  const [payments, setPayments] = useState([]);
  useEffect(() => {
    const token = getToken();
    axios.get(`${API_BASE_URL}/payments`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => setPayments(r.data.slice(0, 8)))
      .catch(e => console.error(e));
  }, []);
  return (
    <ul style={{ paddingLeft: 12 }}>
      {payments.map(p => (
        <li key={p.id} style={{ marginBottom: 8 }}>
          <strong>#{p.id}</strong> — ₦{p.amount} — <small>{p.status}</small>
        </li>
      ))}
    </ul>
  );
}
