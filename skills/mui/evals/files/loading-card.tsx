import CircularProgress from '@mui/material/CircularProgress';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

export function LoadingCard() {
  return (
    <Card>
      <CardContent aria-busy="true">
        <CircularProgress aria-label="Loading" />
      </CardContent>
    </Card>
  );
}
