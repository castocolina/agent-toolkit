import { useEffect, useState } from 'react';

type Result<T> =
  | { status: 'success'; key: string; data: T }
  | { status: 'error'; key: string; error: unknown };

// Fetch hook: the retained result is tagged with the url it belongs to.
export function useJson<T>(url: string): { status: 'loading' } | Result<T> {
  const [result, setResult] = useState<Result<T> | null>(null);

  useEffect(() => {
    let ignore = false;
    const controller = new AbortController();
    fetch(url, { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<T>;
      })
      .then(
        (data) => { if (!ignore) setResult({ status: 'success', key: url, data }); },
        (error) => { if (!ignore) setResult({ status: 'error', key: url, error }); },
      );
    return () => {
      ignore = true;
      controller.abort();
    };
  }, [url]);

  if (result === null || result.key !== url) return { status: 'loading' };
  return result;
}
