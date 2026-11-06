import { useEffect, useState } from 'react';

type Hit = { id: string; title: string };

export function SearchResults({ query }: { query: string }) {
  const [hits, setHits] = useState<Hit[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let ignore = false;
    const controller = new AbortController();
    setLoading(true);
    setError(null);

    fetch(`/api/search?q=${encodeURIComponent(query)}`, { signal: controller.signal })
      .then((res) => res.json())
      .then((json: { hits?: Hit[] }) => {
        if (!ignore) setHits(json.hits ?? []);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));

    return () => {
      ignore = true;
      controller.abort();
    };
  }, [query]);

  if (loading) return <p>Searching...</p>;
  if (error) return <p role="alert">Request failed: {error}</p>;
  return (
    <ul>
      {hits.map((hit) => (
        <li key={hit.id}>{hit.title}</li>
      ))}
    </ul>
  );
}
