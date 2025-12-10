import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import useDeviceLogs, { DeviceLog } from '../hooks/GetDeviceLogs';

interface ApiDevice {
  id: number;
  name: string;
  device_type: string;
  status: string;
  brand?: string | null;
  model?: string | null;
  ip_address?: string | null;
  mac_address?: string | null;
  room?: { id: number; name: string } | null;
  category?: { id: number; name: string; icon?: string } | null;
}

const DeviceDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [device, setDevice] = useState<ApiDevice | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { deviceLogs, loading: logsLoading, error: logsError } = useDeviceLogs(id);

  useEffect(() => {
    
    const fetchDevice = async () => {
      if (!id) return;
      try {
        const base = process.env.REACT_APP_API_BASE_URL || '';
        const res = await axios.get<ApiDevice>(`${base}/api/v1/devices/${id}`);
        setDevice(res.data);

      } catch (err: any) {
        setError(
          err?.response?.data?.error || err.message || 'Failed to fetch device',
        );
      } finally {
        setLoading(false);
      }
    };
    fetchDevice();
    
  }, [id]);

  if (loading) return <p>Loading device...</p>;
  if (error) return <p style={{ color: 'salmon' }}>{error}</p>;
  if (!device) return <p>No device found.</p>;

  return (
    <div>
      <Link to="/">← Back to devices</Link>
      <h2>{device.name}</h2>
      <p>Type: {device.device_type}</p>
      <p>Status: {device.status}</p>
      <p>Brand: {device.brand ?? '—'}</p>
      <p>Model: {device.model ?? '—'}</p>
      <p>IP: {device.ip_address ?? '—'}</p>
      <p>MAC: {device.mac_address ?? '—'}</p>
      <p>Room: {device.room?.name ?? '—'}</p>
      <p>Category: {device.category?.name ?? '—'}</p>
      <h2>Device Logs</h2>
      <ul>
        {logsLoading && <li>Loading logs…</li>}
        {logsError && <li style={{ color: 'salmon' }}>{logsError}</li>}
        {deviceLogs.map((log: DeviceLog) => (
          <li key={log.id}>{log.action} - {log.old_value ?? '—'} to {log.new_value ?? '—'} at {log.timestamp ?? '—'}</li>
        ))}
      </ul>
    </div>
  );
};

export default DeviceDetail;
