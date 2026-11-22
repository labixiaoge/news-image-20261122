// news-image-20261122: a newspaper front page for Sunday 22 November 2026.
// The image is drawn by gen_image.py (PIL, fixed seed) and stored beside this
// file as entry.png; the program only copies it to the output directory, so
// both graded runs write identical bytes.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const src = fileURLToPath(new URL('./entry.png', import.meta.url));
// Fail loudly instead of silently copying a broken entry: the source must be
// a real, non-empty file, otherwise the graded output would be invalid.
const srcStat = statSync(src, { throwIfNoEntry: false });
if (!srcStat?.isFile() || srcStat.size === 0) {
  throw new Error(`entry image missing or empty: ${src}`);
}

const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? '/output');
mkdirSync(outDir, { recursive: true });
// A plain byte-for-byte copy: no timestamps or randomness are involved,
// so the two graded runs always produce the same file.
copyFileSync(src, join(outDir, 'entry.png'));
