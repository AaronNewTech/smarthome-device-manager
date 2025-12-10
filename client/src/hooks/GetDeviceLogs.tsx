import axios from 'axios';
import { useState, useEffect } from 'react';

// Type for device log returned by the API
export interface DeviceLog {
  id: string;
  action: string;
  old_value?: string | null;
  new_value?: string | null;
  timestamp?: string | null;
  device?: string;
}

/**
 * Hook to fetch logs for a given device id (UUID string).
 * Pass `deviceId` (string) and the hook will fetch when it's available.
 */
const useDeviceLogs = (deviceId?: string) => {
  const [deviceLogs, setDeviceLogs] = useState<DeviceLog[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!deviceId) {
      setDeviceLogs([]);
      setLoading(false);
      setError(null);
      return;
    }

    let cancelled = false;
    const fetchDeviceLogs = async () => {
      setLoading(true);
      try {
        const base = process.env.REACT_APP_API_BASE_URL || '';
        // ensure trailing slash to avoid redirects
        const url = `${base}/api/v1/devices/${deviceId}/logs/`;
        const response = await axios.get<DeviceLog[]>(url);
        if (!cancelled) setDeviceLogs(response.data);
      } catch (err: any) {
        const msg =
          err?.response?.data?.detail ||
          err?.message ||
          'Failed to fetch device logs';
        if (!cancelled) setError(String(msg));
      } finally {
        if (!cancelled) setLoading(false);
      }
    };

    fetchDeviceLogs();

    return () => {
      cancelled = true;
    };
  }, [deviceId]);

  return { deviceLogs, loading, error } as const;
};

export default useDeviceLogs;
