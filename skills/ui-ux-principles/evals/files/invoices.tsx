import './invoices.css';

type Invoice = { id: string; customer: string; due: string; amount: string };

export function InvoiceTable({ invoices }: { invoices: Invoice[] }) {
  if (invoices.length === 0) {
    return (
      <p className="invoices">
        No invoices yet. <a href="/invoices/new">Create an invoice</a>
      </p>
    );
  }

  return (
    <section className="invoices">
      <h2>Invoices</h2>
      <div className="table-scroll" role="region" aria-label="Invoices table" tabIndex={0}>
        <table>
          <thead>
            <tr><th>Invoice</th><th>Customer</th><th>Due</th><th>Amount</th></tr>
          </thead>
          <tbody>
            {invoices.map((inv) => (
              <tr key={inv.id}><td>{inv.id}</td><td>{inv.customer}</td><td>{inv.due}</td><td>{inv.amount}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
