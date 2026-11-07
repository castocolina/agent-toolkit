import Dialog from '@mui/material/Dialog/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

interface RenameDialogProps {
  open: boolean;
  onCancel: () => void;
  onSave: () => void;
}

export function RenameDialog({ open, onCancel, onSave }: RenameDialogProps) {
  return (
    <Dialog
      open={open}
      onBackdropClick={onCancel}
      components={{ Backdrop: undefined }}
      componentsProps={{ backdrop: { invisible: true } }}
    >
      <DialogTitle>Rename project</DialogTitle>
      <DialogContent>
        <TextField label="Name" inputProps={{ maxLength: 40 }} />
        <Button onClick={onSave}>Save</Button>
      </DialogContent>
    </Dialog>
  );
}
