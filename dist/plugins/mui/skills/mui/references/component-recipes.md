# MUI component recipes: v7 code

Load this when the user asks for an example of a form field, a form, Stack layout, Card, List, Autocomplete, Snackbar, Dialog, Popover, Menu or Avatar. The traps (slots, Grid size, imports, accessible names) are in `SKILL.md`; this file is working code in the shape the v7 docs show, written to stay valid on v9 too. Checked against mui.com on 2026-11-07 (component pages and API pages under https://mui.com/material-ui/); component props change between minors, so confirm a prop in the installed `<Component>.d.ts` before relying on it.

Two rules hold for every snippet:

- Style through `sx`, not system props: `mt`, `color` and similar props on `Box`, `Grid`, `Stack` and `Typography` are removed in v9 (https://mui.com/material-ui/migration/upgrade-to-v9/), and `sx` works on v7 and v9. `Typography` below uses `sx={{ color: 'text.secondary' }}` for that reason.
- A list row that acts on click is `ListItemButton`. `ListItem` has no `button` prop (https://mui.com/material-ui/api/list-item/); old code with `<ListItem button>` is migrated to `ListItem` wrapping `ListItemButton`.

## TextField with validation

```tsx
<TextField
  id="email"
  label="Email"
  type="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={Boolean(emailError)}
  helperText={emailError}
  fullWidth
  required
/>
```

Give every `TextField` a unique `id`: the docs link the label and helper text through it and warn that a field rendered before hydration has no label association without one (https://mui.com/material-ui/react-text-field/). Native `<input>` attributes (`aria-label`, `data-testid`, `maxLength`) go in `slotProps={{ htmlInput: { ... } }}`, not `slotProps.input`, which targets the MUI Input component.

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

## Card

```tsx
<Card>
  <CardMedia component="img" height="200" image="/image.jpg" alt="Describe the picture" />
  <CardContent>
    <Typography variant="h5" component="h2" gutterBottom>
      Card title
    </Typography>
    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
      Card description text
    </Typography>
  </CardContent>
  <CardActions>
    <Button size="small">Learn more</Button>
    <Button size="small">Share</Button>
  </CardActions>
</Card>
```

`CardMedia` renders a `div` with a background image unless `component` is set (`img`, `video`), and only an `img` carries `alt`; use a decorative `alt=""` when the picture adds nothing. For a card whose whole surface is one action, wrap the content in `CardActionArea` and keep supplemental buttons outside it so their events do not overlap (https://mui.com/material-ui/react-card/).

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

## Dialog

```tsx
<Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
  <DialogTitle>Confirm delete</DialogTitle>
  <DialogContent>
    <DialogContentText>
      Are you sure you want to delete this item? This action cannot be undone.
    </DialogContentText>
  </DialogContent>
  <DialogActions>
    <Button onClick={handleClose}>Cancel</Button>
    <Button onClick={handleDelete} color="error" variant="contained">
      Delete
    </Button>
  </DialogActions>
</Dialog>
```

Keep `open` controlled by the parent and keep `DialogTitle`, which names the dialog. Close paths go through `onClose(event, reason)`; to block one, branch on `reason` as the worked branch in `SKILL.md` does. On v9, `disableEscapeKeyDown` is removed from `Dialog` and `Modal`, so block `escapeKeyDown` the same way. For an alert-style confirmation add `role="alertdialog"` (https://mui.com/material-ui/react-dialog/).

## Popover

```tsx
const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);
const open = Boolean(anchorEl);
const id = open ? 'details-popover' : undefined;

<Button aria-describedby={id} variant="contained" onClick={(e) => setAnchorEl(e.currentTarget)}>
  Details
</Button>
<Popover
  id={id}
  open={open}
  anchorEl={anchorEl}
  onClose={() => setAnchorEl(null)}
  anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
>
  <Typography sx={{ p: 2 }}>Popover content</Typography>
</Popover>
```

`Popover` is built on `Modal`: it blocks page scroll and closes on click-away. For a hint that must not block the page, use `Popper` (https://mui.com/material-ui/react-popover/).

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

## Avatar

```tsx
<Stack direction="row" spacing={2}>
  <Avatar src="/avatar.jpg" alt="Jane Doe" />
  <Avatar sx={{ bgcolor: 'primary.main' }}>JD</Avatar>
  <Avatar variant="square" src="/logo.png" alt="Company logo" />
  <AvatarGroup max={3}>
    <Avatar src="/user1.jpg" alt="User 1" />
    <Avatar src="/user2.jpg" alt="User 2" />
    <Avatar src="/user3.jpg" alt="User 3" />
    <Avatar src="/user4.jpg" alt="User 4" />
  </AvatarGroup>
</Stack>
```

When an image fails to load, `Avatar` falls back to its children, then the first letter of `alt`, then a generic icon, so a real name in `alt` gives a sensible fallback (https://mui.com/material-ui/react-avatar/). `AvatarGroup` collapses the extra avatars past `max` into a count.

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
