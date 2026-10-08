import React from 'react';

export default function DocIndex({ children }) {
  return (
    <div className="doc_index">
      <ul>{children}</ul>
    </div>
  );
}
