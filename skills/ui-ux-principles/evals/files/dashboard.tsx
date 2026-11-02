import { useEffect, useState } from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

type Order = { id: string; customer: string; total: number };

export function OrdersDashboard() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/orders')
      .then((r) => r.json())
      .then((data) => setOrders(data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <div style={{ width: 1200, display: 'flex' }}>
      <aside style={{ width: 240 }}>Filters</aside>
      <ul style={{ width: 960 }}>
        {orders.map((o) => (
          <li key={o.id} style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{o.customer}</span>
            <span>{o.total}</span>
            <IconButton onClick={() => fetch(`/api/orders/${o.id}`, { method: 'DELETE' })}>
              <DeleteIcon />
            </IconButton>
          </li>
        ))}
      </ul>
    </div>
  );
}
