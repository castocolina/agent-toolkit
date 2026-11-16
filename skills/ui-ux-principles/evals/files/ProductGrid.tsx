import { useState } from 'react';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogTitle from '@mui/material/DialogTitle';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';

type Product = { id: string; name: string; price: string };

export function ProductGrid({ products, onAdd, onDeleteList }: {
  products: Product[];
  onAdd: (id: string) => void;
  onDeleteList: () => void;
}) {
  const [confirming, setConfirming] = useState(false);

  return (
    <>
      <Grid container spacing={2}>
        {products.map((p) => (
          <Grid key={p.id} size={{ xs: 12, sm: 6, md: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h6">{p.name}</Typography>
                <Typography color="text.secondary">{p.price}</Typography>
              </CardContent>
              <CardActions>
                <Button variant="contained" onClick={() => onAdd(p.id)}>Add to cart</Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
      <Button color="error" onClick={() => setConfirming(true)}>Delete list</Button>
      <Dialog open={confirming} onClose={() => setConfirming(false)}>
        <DialogTitle>Delete this product list?</DialogTitle>
        <DialogActions>
          <Button onClick={() => setConfirming(false)}>Cancel</Button>
          <Button variant="contained" color="error" onClick={onDeleteList}>Delete</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
