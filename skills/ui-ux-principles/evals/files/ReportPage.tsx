type ReportRow = { id: string; label: string; value: string };

function ReportPanel({ rows }: { rows: ReportRow[] }) {
  return (
    <section aria-label="Quarterly report" style={{ width: 900 }}>
      <dl>
        {rows.map((row) => (
          <div key={row.id}>
            <dt>{row.label}</dt>
            <dd>{row.value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}

export function ReportPage({ rows }: { rows: ReportRow[] }) {
  return (
    <div style={{ display: 'flex' }}>
      <nav aria-label="Report sections" style={{ width: 240 }}>
        <a href="#summary">Summary</a>
      </nav>
      <ReportPanel rows={rows} />
    </div>
  );
}
