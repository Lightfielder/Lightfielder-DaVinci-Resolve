import React from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useCurrentSidebarCategory } from '@docusaurus/plugin-content-docs/client';
import { TYPE_CONFIG, FUNCTION_CONFIG } from '@site/src/data/categoryConfig';

/**
 * Card grid for a category's overview page. Reads the current sidebar category
 * (so counts + links stay in sync with the docs automatically) and renders one
 * card per subcategory with an icon pill, name, item count and a one-line
 * description. Plain CSS classes live in src/css/custom.css.
 *
 * Usage:
 *   <CategoryCards variant="types" family="Core" />  // Level 1 (family -> data types)
 *   <CategoryCards />                                 // Level 2 (data type -> function groups)
 *
 * On Level 1 the icons are real SVG files at static/img/icons/<Family>_<Label>.svg
 * — the naming matches every data-type card in both families. Those files have
 * their baked-in tile background stripped out, so the colour comes from the CSS
 * tile (.cat-card-icon--<color>) and only the line art is masked in, painted in
 * currentColor. Pass `family` so the right artwork set is resolved.
 */
export default function CategoryCards({ variant = 'functions', family }) {
  const category = useCurrentSidebarCategory();
  const items = (category && category.items) || [];
  const config = variant === 'types' ? TYPE_CONFIG : FUNCTION_CONFIG;
  const iconsBase = useBaseUrl('/img/vonkultra/icons/');

  const cards = items
    .map((item) => {
      const cfg = config[item.label] || {};
      const count = item.items?.length ?? 1;
      // Level 1 data types have SVG artwork named <Family>_<Label>.svg. Levels 2
      // and 3 are function groups, which have no artwork, so they keep the glyph.
      const svg =
        variant === 'types' && family
          ? `${iconsBase}${family}_${item.label}.svg`
          : null;
      return { label: item.label, href: item.href, count, icon: cfg.icon || item.label, color: cfg.color || 'default', desc: cfg.desc || '', svg };
    })
    .filter((c) => c.href);

  if (!cards.length) return null;

  return (
    <div className="cat-cards">
      {cards.map((c) => (
        <Link key={c.label} className="cat-card" to={c.href}>
          <span className={`cat-card-icon cat-card-icon--${c.color}`}>
            {c.svg ? (
              <span
                className="cat-card-icon-glyph"
                style={{'--cat-card-icon': `url("${c.svg}")`}}
              />
            ) : (
              c.icon
            )}
          </span>
          <span className="cat-card-body">
            <span className="cat-card-title">
              {c.label}
              <span className="cat-card-count">
                {c.count} item{c.count === 1 ? '' : 's'}
              </span>
            </span>
            {c.desc && <span className="cat-card-desc">{c.desc}</span>}
          </span>
        </Link>
      ))}
    </div>
  );
}
