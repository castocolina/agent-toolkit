import Dialog from '@mui/material/Dialog/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';

interface MigrationDialogProps {
  open: boolean;
  onClose: () => void;
  projectName: string;
}

export function MigrationDialog({ open, onClose, projectName }: MigrationDialogProps) {
  return (
    <Dialog open={open} onBackdropClick={onClose} components={{ Backdrop: undefined }}>
      <DialogTitle>Delete {projectName}?</DialogTitle>
      <DialogContent>
        <Grid container>
          <Grid item xs={12} md={6}>
            This permanently deletes the project and its deployments.
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button color="error" onClick={onClose}>Delete</Button>
      </DialogActions>
    </Dialog>
  );
}
