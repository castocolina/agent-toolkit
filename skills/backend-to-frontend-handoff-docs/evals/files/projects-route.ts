router.patch('/api/projects/:id', requireAuth('projects:write'), async (req, res) => {
  const body = parse(UpdateProjectDto, req.body); // title: string, 1-80 chars; dueDate: ISO date string or null
  const p = await db.projects.find(req.params.id);
  if (!p) throw new NotFound();
  if (p.ownerId !== req.user.id) throw new Forbidden('not_owner');
  if (body.title !== undefined) p.title = body.title;
  if ('dueDate' in body) p.due = body.dueDate; // null clears the due date, an omitted key leaves it unchanged
  res.status(200).json(serializeProject(await db.projects.save(p)));
});

router.use((err, req, res, next) => {
  if (err instanceof ValidationError) return res.status(400).json({ code: 'invalid_body', fields: err.fields });
  if (err instanceof Forbidden) return res.status(403).json({ code: err.reason });
  if (err instanceof NotFound) return res.status(404).json({ code: 'not_found' });
  next(err);
});
