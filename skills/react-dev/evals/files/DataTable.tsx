// src/components/DataTable.tsx
import type { ReactNode } from 'react';

export type Column<T> = {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], row: T) => ReactNode;
};

export function DataTable<T>({ rows, columns, rowKey }: { rows: T[]; columns: Column<T>[]; rowKey: (row: T) => string }) {
  return (
    <table>
      <tbody>
        {rows.map((row) => (
          <tr key={rowKey(row)}>
            {columns.map((c) => (
              <td key={String(c.key)}>{c.render ? c.render(row[c.key], row) : String(row[c.key])}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// src/pages/Invoices.tsx
type Invoice = { id: string; customer: string; dueDate: Date; total: number };

export const invoiceColumns: Column<Invoice>[] = [
  { key: 'customer', header: 'Customer' },
  // Compiles, then crashes at runtime: dueDate is a Date, not a string.
  { key: 'dueDate', header: 'Due', render: (value) => (value as string).slice(0, 10) },
  { key: 'total', header: 'Total', render: (value) => `$${value}` },
];
