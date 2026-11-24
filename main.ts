// Entry point for the news-image-20261123 submission.
//
// The graded artifact in this competition is the PNG that sits next to
// this file. The runner executes this program in a clean container where
// the repository is mounted read-only and the only writable place is the
// output directory: MAKEFUN_OUTPUT_DIR when that variable is set, and
// /output otherwise. So the whole job here is to deliver the image into
// that directory under the name entry.png, byte for byte. The runner
// executes the program twice, which means the delivery has to be
// idempotent: same input, same output, no state carried between runs.

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const IMAGE_NAME = 'entry.png';

// The source image lives beside this module. Resolving it relative to
// import.meta.url keeps the program independent of whatever working
// directory the runner happens to start it from.
function sourceImagePath() {
  const moduleDir = dirname(fileURLToPath(import.meta.url));
  return join(moduleDir, IMAGE_NAME);
}

function destinationImagePath() {
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
  return join(outputDir, IMAGE_NAME);
}

function publishImage() {
  const from = sourceImagePath();
  const to = destinationImagePath();
  // The documented local test flow points MAKEFUN_OUTPUT_DIR at a folder
  // that may not exist yet, so create the destination directory first.
  mkdirSync(dirname(to), { recursive: true });
  copyFileSync(from, to);
  return { from, to };
}

// The judge grades exactly the bytes that land in the output directory,
// so a copy that silently came out short would score a different image
// than the one drawn. Compare the delivered size against the source and
// refuse to report success when they disagree.
function verifyDelivery(from, to) {
  const expected = statSync(from).size;
  const actual = statSync(to).size;
  if (actual !== expected) {
    throw new Error(`delivered image is ${actual} bytes, source is ${expected} bytes`);
  }
  return actual;
}

try {
  const { from, to } = publishImage();
  const size = verifyDelivery(from, to);
  console.log(`entry image delivered to ${to} (${size} bytes, verified)`);
} catch (error) {
  console.error(`failed to deliver entry image: ${error.message}`);
  process.exit(1);
}
