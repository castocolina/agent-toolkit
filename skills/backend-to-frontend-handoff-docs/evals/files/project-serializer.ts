export function serializeProject(p: ProjectRow) {
  return {
    id: p.id,
    name: p.title,
    dueOn: p.due ?? null,
    ...(p.archivedAt ? { archivedAt: p.archivedAt.toISOString() } : {}),
  };
}
