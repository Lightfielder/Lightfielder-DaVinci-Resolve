/**
 * Single source of truth for the 3-level overview system's card configs.
 *
 * Imported by:
 *   - src/components/CategoryCards.jsx  (Level 1 + Level 2 cards)
 *   - src/theme/DocCard/index.js        (Level 3 node-card icons)
 *   - tools/update-function-descriptions.mjs (Level 3 H1 intros)
 *
 * Every entry: { icon, color, desc } — `color` is used as the CSS class
 * suffix (`cat-card-icon--<color>` solid, `doc-group-icon--<color>` light).
 */

// ---- Level 1: data types -------------------------------------------------
export const TYPES = {
  Array: { icon: '[ ]', color: 'array', desc: 'Handle collections of data and sequential operations.' },
  HTML: { icon: '</>', color: 'html', desc: 'Render and parse structured markup content.' },
  JSON: { icon: 'JS', color: 'json', desc: 'Manipulate objects and hierarchical data structures.' },
  Matrix: { icon: '#', color: 'matrix', desc: 'Transform coordinates and handle 3D space operations.' },
  Number: { icon: '123', color: 'number', desc: 'Perform mathematical functions and scalar calculations.' },
  ScriptVal: { icon: '<>', color: 'scriptval', desc: 'Execute dynamic expressions and scripting values.' },
};

export const CORE_TYPES = {
  '3D': { icon: '3D', color: 'type-3d', desc: 'Work with 3D points, geometry, and scene data.' },
  Base64: { icon: '64', color: 'type-base64', desc: 'Encode and decode data as Base64 text.' },
  CBOR: { icon: '{}', color: 'type-cbor', desc: 'Serialize and deserialize compact binary data.' },
  Color: { icon: '◉', color: 'type-color', desc: 'Create, convert, and manipulate color values.' },
  FileSystem: { icon: 'FS', color: 'type-filesystem', desc: 'Read, write, and manage files and folders.' },
  Gradient: { icon: '◔', color: 'type-gradient', desc: 'Create and manipulate color gradients.' },
  Guide: { icon: '⊞', color: 'type-guide', desc: 'Reference guides and on-screen helpers.' },
  Image: { icon: '▣', color: 'type-image', desc: 'Load, process, and save image data.' },
  Meta: { icon: 'ⓘ', color: 'type-meta', desc: 'Read and write metadata records.' },
  MTLX: { icon: 'MX', color: 'type-mtlx', desc: 'MaterialX material definitions.' },
  Point: { icon: '•', color: 'type-point', desc: '2D/3D points and coordinate math.' },
  Shape: { icon: '◇', color: 'type-shape', desc: 'Shape primitives and geometry.' },
  Text: { icon: 'T', color: 'type-text', desc: 'String manipulation and text processing.' },
  USD: { icon: '◧', color: 'type-usd', desc: 'Universal Scene Description data.' },
  Vector: { icon: '↗', color: 'type-vector', desc: 'Vectors and directional math.' },
  YAML: { icon: 'Y', color: 'type-yaml', desc: 'Serialize and parse YAML data.' },
};

// ---- Level 2: function groups --------------------------------------------
export const FUNCTION_GROUPS = {
  Accumulate: { icon: '∑', color: 'accumulate', desc: 'Build up values and carry state across frames.' },
  Animate: { icon: '◐', color: 'animate', desc: 'Animate and ease point properties over time.' },
  Create: { icon: '+', color: 'create', desc: 'Generate new arrays, point sets, and objects.' },
  IO: { icon: '⇄', color: 'io', desc: 'Import and export data in and out of the pipeline.' },
  Logic: { icon: '∧', color: 'logic', desc: 'Compare, filter, and branch on values.' },
  Modify: { icon: '~', color: 'modify', desc: 'Transform, deform, and remap point data.' },
  OBJ: { icon: '◎', color: 'obj', desc: 'Bring 3D geometry in and out of point data.' },
  ShapeRender: { icon: '◇', color: 'shaperender', desc: 'Draw dots, lines, shapes, and glyphs from points.' },
  Shapes: { icon: '◧', color: 'shapes', desc: 'Create ready-made shapes and forms.' },
  Temporal: { icon: '↻', color: 'temporal', desc: 'Time-based effects, delays, and frame offsets.' },
  Trigonometry: { icon: '∠', color: 'trigonometry', desc: 'Trigonometric functions and angle math.' },
  Utility: { icon: '⚙', color: 'utility', desc: 'Converters, helpers, and data plumbing.' },
};

export const CORE_FUNCTION_GROUPS = {
  Array: { icon: '[]', color: 'fn-array', desc: 'Work with array and list values.' },
  Case: { icon: 'Aa', color: 'fn-case', desc: 'Change and transform text case.' },
  Color: { icon: '◉', color: 'fn-color', desc: 'Create and convert color values.' },
  Comp: { icon: '▣', color: 'fn-comp', desc: 'Composition and host metadata.' },
  'Custom Data': { icon: '▤', color: 'fn-custom-data', desc: 'Attach and read custom data records.' },
  Decode: { icon: '⤓', color: 'fn-decode', desc: 'Decode encoded data.' },
  Encode: { icon: '⤒', color: 'fn-encode', desc: 'Encode data into another format.' },
  Flow: { icon: '⇶', color: 'fn-flow', desc: 'Routing, branching, and control flow.' },
  Font: { icon: 'A', color: 'fn-font', desc: 'Font metrics and font list operations.' },
  Fusion: { icon: 'F', color: 'fn-fusion', desc: 'Fusion API and host integration.' },
  Image: { icon: '▣', color: 'fn-image', desc: 'Image data helpers.' },
  JSON: { icon: '{}', color: 'fn-json', desc: 'JSON serialize and parse helpers.' },
  'Key Value': { icon: '⇄', color: 'fn-key-value', desc: 'Key/value map operations.' },
  Matte: { icon: '◫', color: 'fn-matte', desc: 'Alpha, matte, and channel data.' },
  Matrix: { icon: '⊞', color: 'fn-matrix', desc: 'Matrix construction and math.' },
  Meta: { icon: 'ⓘ', color: 'fn-meta', desc: 'Metadata helpers.' },
  Number: { icon: '123', color: 'fn-number', desc: 'Number conversion and math.' },
  Operators: { icon: '∔', color: 'fn-operators', desc: 'Math and logic operators.' },
  Order: { icon: '⇅', color: 'fn-order', desc: 'Sorting and ordering values.' },
  Pixel: { icon: '◨', color: 'fn-pixel', desc: 'Pixel-level image data.' },
  Point: { icon: '•', color: 'fn-point', desc: 'Point construction and math.' },
  Resolve: { icon: '✓', color: 'fn-resolve', desc: 'Resolve IDs and values.' },
  Script: { icon: 'λ', color: 'fn-script', desc: 'Run Lua scripts.' },
  ScriptVal: { icon: '<>', color: 'fn-scriptval', desc: 'ScriptVal data helpers.' },
  Shape: { icon: '◇', color: 'fn-shape', desc: 'Shape helpers.' },
  Substring: { icon: '✂', color: 'fn-substring', desc: 'Extract and replace substrings.' },
  Subtitle: { icon: '✎', color: 'fn-subtitle', desc: 'Subtitle and caption text.' },
  Surface: { icon: '◖', color: 'fn-surface', desc: 'Material surface helpers.' },
  Text: { icon: 'T', color: 'fn-text', desc: 'Text helpers.' },
  Transform: { icon: '⇱', color: 'fn-transform', desc: 'Matrix transforms and space conversion.' },
  Vector: { icon: '→', color: 'fn-vector', desc: 'Vector helpers.' },
  XML: { icon: '<?>', color: 'fn-xml', desc: 'XML parse and serialize helpers.' },
  YAML: { icon: 'Y', color: 'fn-yaml', desc: 'YAML helpers.' },
};

// ---- Merged lookups (labels are unique within each family/level) ---------
export const TYPE_CONFIG = { ...TYPES, ...CORE_TYPES };
export const FUNCTION_CONFIG = { ...FUNCTION_GROUPS, ...CORE_FUNCTION_GROUPS };

// label -> icon, for the Level-3 DocCard swizzle
export const FUNCTION_ICONS = Object.fromEntries(
  Object.entries(FUNCTION_CONFIG).map(([label, cfg]) => [label, cfg.icon]),
);
