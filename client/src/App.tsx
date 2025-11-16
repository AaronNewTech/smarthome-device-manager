import React from 'react';
import './App.css';

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import DeviceCard from './components/DeviceCard';
import GetDevices, { Device as DeviceType } from './hooks/GetDevices';
import axios from 'axios';
import DeviceDetail from './pages/DeviceDetail';

function AppInner() {
  const { devices, loading, error } = GetDevices();

  const fetchDeviceLogs = async (id: number) => {
    try {
      const base = process.env.REACT_APP_API_BASE_URL || '';
      const res = await axios.get(`${base}/api/devices/${id}/logs`);
      console.log(`Logs for device ${id}:`, res.data);
    } catch (err) {
      console.warn('Failed to fetch device logs for', id, err);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Home Device Manager</h1>

        {loading && <p>Loading devices…</p>}
        {error && <p style={{ color: 'salmon' }}>{error}</p>}

        <div className="device-list">
          {devices.map((d: DeviceType) => (
            <DeviceCard
              key={d.id}
              device={d}
              fetchDeviceLogs={fetchDeviceLogs}
            />
          ))}
        </div>
      </header>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppInner />} />
        <Route path="/devices/:id" element={<DeviceDetail />} />
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;
