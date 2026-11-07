import { mkdirSync, writeFileSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

// Created once and reused on every run; nothing in the repo ever deletes it.
export const tempDir = join(process.env.HOME ?? ".", ".editor-drafts");
mkdirSync(tempDir, { recursive: true });

// Unsaved user drafts live here; they cannot be rebuilt from anywhere else.
export function saveDraft(id: string, text: string): void {
  writeFileSync(join(tempDir, `${id}.draft`), text);
}

export function loadDraft(id: string): string | null {
  const path = join(tempDir, `${id}.draft`);
  return existsSync(path) ? readFileSync(path, "utf8") : null;
}
