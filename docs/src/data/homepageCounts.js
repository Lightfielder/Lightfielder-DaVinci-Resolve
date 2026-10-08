/**
 * PROTOTYPE ONLY — shared node counts for the landing-page prototypes.
 *
 * Measured from docs/reference/** (see 01-content-inventory/README.md).
 * If a landing page is adopted for real, these should be generated at build
 * time rather than hardcoded — the global CategoryCards derives its counts
 * from the sidebar, which isn't available outside a docs category page.
 */

export const MOG_COUNTS = {
  Array: 185,
  JSON: 182,
  ScriptVal: 182,
  Number: 7,
  Matrix: 3,
  HTML: 2,
};

export const CORE_COUNTS = {
  Text: 88,
  Number: 83,
  ScriptVal: 61,
  Array: 29,
  Matrix: 25,
  Point: 25,
  Gradient: 21,
  Image: 18,
  FileSystem: 17,
  JSON: 14,
  Vector: 14,
  Base64: 7,
  Meta: 7,
  '3D': 5,
  Guide: 5,
  CBOR: 4,
  Color: 3,
  MTLX: 3,
  Shape: 2,
  USD: 2,
  YAML: 1,
};

export const sum = (counts) => Object.values(counts).reduce((a, b) => a + b, 0);

export const TOTAL = sum(MOG_COUNTS) + sum(CORE_COUNTS);
export const DATA_TYPE_COUNT = Object.keys(MOG_COUNTS).length + Object.keys(CORE_COUNTS).length;
