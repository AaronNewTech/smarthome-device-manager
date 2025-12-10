import axios from 'axios';
import { useState, useEffect } from 'react';

// Matches the raw API shape returned by the Django backend
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

// Simplified shape that the UI components may expect
export interface Device {
  id: number;
  name: string;
  type: string;
  status: string;
  roomName?: string | null;
}

const GetDevices = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        // If your React dev server runs on a different port, set REACT_APP_API_BASE_URL
        // (e.g. http://localhost:5000) or configure a proxy in package.json
        // Ensure base has no trailing slash, then request the API with a trailing slash
        const rawBase = process.env.REACT_APP_API_BASE_URL || '';
        const base = rawBase.replace(/\/$/, '');
        console.log('Fetching devices from API at', `${base}/api/v1/devices/`);
        const response = await axios.get<ApiDevice[]>(
          `${base}/api/v1/devices/`,
        );

        // Map API shape to the simplified UI shape (keeps TS types correct)
        const mapped: Device[] = response.data.map((d) => ({
          id: d.id,
          name: d.name,
          type: d.device_type,
          status: d.status,
          roomName: d.room?.name ?? null,
        }));
        // console.log(mapped)
        setDevices(mapped);
      } catch (err: any) {
        // capture server error message when available
        const msg =
          err?.response?.data?.error ||
          err?.message ||
          'Failed to fetch devices';
        setError(String(msg));
      } finally {
        setLoading(false);
      }
    };

    fetchDevices();
  }, []);

  return { devices, loading, error };
};

export default GetDevices;
