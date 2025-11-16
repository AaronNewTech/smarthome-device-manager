import { useEffect } from 'react';
import { Link } from 'react-router-dom';

interface Device {
  id: number;
  name: string;
  status: string;
  lastActive?: string | number | Date | null;
}

interface DeviceCardProps {
  device: Device;
  fetchDeviceLogs?: (id: number) => void;
}

const DeviceCard = ({ device, fetchDeviceLogs }: DeviceCardProps) => {
  // Fetch logs when the card mounts (if a fetch function is provided)
  useEffect(() => {
    if (fetchDeviceLogs) fetchDeviceLogs(device.id);
  }, [device.id, fetchDeviceLogs]);

  return (
    <Link
      to={`/devices/${device.id}`}
      className="device-card"
      style={{ textDecoration: 'none', color: 'inherit' }}
    >
      <div>
        <h3>{device.name}</h3>
        <p>Status: {device.status}</p>
        <p>
          Last Active:{' '}
          {device.lastActive
            ? new Date(device.lastActive).toLocaleString()
            : '—'}
        </p>
      </div>
    </Link>
  );
};

export default DeviceCard;
