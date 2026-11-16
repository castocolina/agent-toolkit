# MUI component recipes: v7 code

Load this when the user asks for an example of a form, Stack layout, List, Autocomplete, Snackbar or Menu. The traps (slots, Grid size, imports, accessible names) are in `SKILL.md`; this file is working code in the shape the v7 docs show, written to stay valid on v9 too. Checked against mui.com on 2026-11-07 (component pages and API pages under https://mui.com/material-ui/); component props change between minors, so confirm a prop in the installed `<Component>.d.ts` before relying on it.

Two rules hold for every snippet:

- Style through `sx`, not system props: `mt`, `color` and similar props on `Box`, `Grid`, `Stack` and `Typography` are removed in v9 (https://mui.com/material-ui/migration/upgrade-to-v9/), and `sx` works on v7 and v9.
- A list row that acts on click is `ListItemButton`. `ListItem` has no `button` prop (https://mui.com/material-ui/api/list-item/); old code with `<ListItem button>` is migrated to `ListItem` wrapping `ListItemButton`.

## Stack

One-dimensional layout with spacing; `direction` and `spacing` accept breakpoint objects:

```tsx
<Stack direction="row" spacing={2} sx={{ alignItems: 'center' }}>
  <Avatar src={user.avatar} alt={user.name} />
  <Typography>{user.name}</Typography>
  <Chip label={user.role} />
</Stack>

<Stack direction={{ xs: 'column', sm: 'row' }} spacing={{ xs: 1, sm: 2 }}>...</Stack>
```

The default spacing is margin-based, so a margin you set on a child is ignored; set `useFlexGap` on the `Stack` to switch to flexbox `gap` (https://mui.com/material-ui/react-stack/).

## List

```tsx
<List>
  <ListItem disablePadding>
    <ListItemButton onClick={handleClick}>
      <ListItemIcon>
        <InboxIcon />
      </ListItemIcon>
      <ListItemText primary="Inbox" secondary="5 new messages" />
    </ListItemButton>
  </ListItem>
  <Divider />
  <ListItem>
    <ListItemAvatar>
      <Avatar src="/avatar.jpg" alt="John Doe" />
    </ListItemAvatar>
    <ListItemText primary="John Doe" secondary="Online" />
  </ListItem>
</List>
```

A `ListItemButton` row sits in a `ListItem disablePadding`, so the button, not the item, owns the padding and the click target. A trailing control (an icon button, a switch) goes in `ListItem`'s `secondaryAction`. For a link row use `<ListItemButton component="a" href="...">`.

## Autocomplete

```tsx
<Autocomplete
  options={options}
  getOptionLabel={(option) => option.label}
  isOptionEqualToValue={(option, selected) => option.id === selected.id}
  value={value}
  onChange={(_event, newValue) => setValue(newValue)}
  renderInput={(params) => <TextField {...params} label="Search" placeholder="Type to search..." />}
/>
```

- `value` and `onChange` hold the selected option; `inputValue` and `onInputChange` hold the typed text. Control them independently.
- Object options need `isOptionEqualToValue` when the selected object is not the same instance as the one in `options`; without it the comparison is strict equality, so a value rebuilt from your own state is not matched to its option (https://mui.com/material-ui/react-autocomplete/).
- The `label` on the `TextField` is the combobox's accessible name; keep it.

## Snackbar

```tsx
<Snackbar
  open={open}
  autoHideDuration={6000}
  onClose={(_event, reason) => {
    if (reason === 'clickaway') return;
    setOpen(false);
  }}
  anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
>
  <Alert onClose={() => setOpen(false)} severity="success" variant="filled" sx={{ width: '100%' }}>
    Changes saved
  </Alert>
</Snackbar>
```

`onClose(event, reason)` reports `timeout`, `clickaway` or `escapeKeyDown` (https://mui.com/material-ui/api/snackbar/). Ignoring `clickaway` keeps the message up until its timer ends or the user dismisses it; leave that line out if a click elsewhere should close it. `autoHideDuration` is `null` by default, so a Snackbar stays open until you set it; give users enough time to read the text. Swap the transition with `slots.transition` and `slotProps.transition`.

## Menu

```tsx
const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
const open = Boolean(anchorEl);

<Button
  id="actions-button"
  aria-controls={open ? 'actions-menu' : undefined}
  aria-haspopup="true"
  aria-expanded={open ? 'true' : undefined}
  onClick={(e) => setAnchorEl(e.currentTarget)}
>
  Actions
</Button>
<Menu
  id="actions-menu"
  anchorEl={anchorEl}
  open={open}
  onClose={() => setAnchorEl(null)}
  slotProps={{ list: { 'aria-labelledby': 'actions-button' } }}
>
  <MenuItem onClick={handleEdit}>
    <ListItemIcon><EditIcon fontSize="small" /></ListItemIcon>
    <ListItemText>Edit</ListItemText>
  </MenuItem>
  <MenuItem onClick={handleDelete}>
    <ListItemIcon><DeleteIcon fontSize="small" /></ListItemIcon>
    <ListItemText>Delete</ListItemText>
  </MenuItem>
</Menu>
```

`Menu`'s `slotProps` accepts `backdrop`, `list`, `paper`, `root` and `transition` (https://mui.com/material-ui/api/menu/). Older code reaches the list through `MenuListProps`; read the installed `Menu.d.ts` to see which name the version declares. Close the menu inside each item handler as well. `onClose` reports `escapeKeyDown`, `backdropClick` or `tabKeyDown`.

## Complete form

A form that uses accessible names and labelled controls throughout. `Select` needs the label in two places and the `labelId` link, or it has no accessible name (https://mui.com/material-ui/react-select/):

```tsx
import type { SelectChangeEvent } from '@mui/material/Select';

<Box component="form" onSubmit={handleSubmit} noValidate sx={{ maxWidth: 600 }}>
  <Stack spacing={3}>
    <TextField
      id="full-name"
      label="Full name"
      required
      fullWidth
      error={Boolean(errors.name)}
      helperText={errors.name}
    />

    <TextField
      id="email"
      label="Email"
      type="email"
      required
      fullWidth
      error={Boolean(errors.email)}
      helperText={errors.email}
    />

    <FormControl fullWidth>
      <InputLabel id="role-label">Role</InputLabel>
      <Select
        labelId="role-label"
        id="role"
        label="Role"
        value={role}
        onChange={(e: SelectChangeEvent) => setRole(e.target.value)}
      >
        <MenuItem value="user">User</MenuItem>
        <MenuItem value="admin">Admin</MenuItem>
      </Select>
    </FormControl>

    <FormControlLabel
      control={<Checkbox checked={agreed} onChange={(e) => setAgreed(e.target.checked)} />}
      label="I agree to the terms and conditions"
    />

    <Stack direction="row" spacing={2} sx={{ justifyContent: 'flex-end' }}>
      <Button variant="outlined" onClick={handleCancel}>
        Cancel
      </Button>
      <Button type="submit" variant="contained" disabled={!agreed}>
        Submit
      </Button>
    </Stack>
  </Stack>
</Box>
```

- `InputLabel id` matches `Select labelId`, and the `label` prop repeats the text for the outlined variant's notch.
- `noValidate` hands validation to your `error` and `helperText` state; drop it to keep the browser's own messages.
- Check each control's name with a role-based query (`getByRole('combobox', { name: 'Role' })`) rather than by eye.
