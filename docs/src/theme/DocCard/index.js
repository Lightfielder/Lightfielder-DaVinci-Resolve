/**
 * Swizzled DocCard.
 *
 * Mirrors the original Kartaverse Vonk Ultra swizzle: on function-group index
 * pages (e.g. Array → Animate) each node card shows that group's icon from the
 * Level-2 overview instead of the default document emoji, using the same
 * `.cat-card` markup as the Level-1/Level-2 category cards.
 *
 * IMPORTANT: this swizzle is global, so the custom rendering is gated to paths
 * under `/VonkUltra/`. Everywhere else the stock Docusaurus DocCard is rendered
 * unchanged — which also keeps `<DocCardList />` usable on non-category pages
 * (the custom version relies on `useCurrentSidebarCategory()`, which throws
 * outside a category index).
 */
import React from 'react';
import OriginalDocCard from '@theme-original/DocCard';
import { useLocation } from '@docusaurus/router';
import {
  useDocById,
  findFirstSidebarItemLink,
  useCurrentSidebarCategory,
} from '@docusaurus/plugin-content-docs/client';
import {
  extractLeadingEmoji,
  useDocCardDescriptionCategoryItemsPlural,
} from '@docusaurus/theme-common/internal';
import isInternalUrl from '@docusaurus/isInternalUrl';
import Link from '@docusaurus/Link';
import Layout from '@theme/DocCard/Layout';
import { FUNCTION_CONFIG } from '@site/src/data/categoryConfig';

function getFallbackEmojiIcon(item) {
  if (item.type === 'category') {
    return '🗃';
  }
  return isInternalUrl(item.href) ? '📄️' : '🔗';
}

function getIconTitleProps(item) {
  const extracted = extractLeadingEmoji(item.label);
  return {
    icon: extracted.emoji ?? getFallbackEmojiIcon(item),
    title: extracted.rest.trim(),
  };
}

function CardCategory({ item }) {
  const href = findFirstSidebarItemLink(item);
  const categoryItemsPlural = useDocCardDescriptionCategoryItemsPlural();
  if (!href) {
    return null;
  }
  return (
    <Layout
      item={item}
      className={item.className}
      href={href}
      description={item.description ?? categoryItemsPlural(item.items.length)}
      {...getIconTitleProps(item)}
    />
  );
}

function CardLink({ item }) {
  const doc = useDocById(item.docId ?? undefined);
  const currentCategory = useCurrentSidebarCategory();
  const group = currentCategory ? FUNCTION_CONFIG[currentCategory.label] : null;
  const description = item.description ?? doc?.description ?? '';
  return (
    <Link href={item.href} className="cat-card">
      <span
        className={`doc-group-icon ${
          group ? `doc-group-icon--${group.color}` : 'doc-group-icon--default'
        }`}>
        {group ? group.icon : getFallbackEmojiIcon(item)}
      </span>
      <span className="cat-card-body">
        <span className="cat-card-title">{item.label}</span>
        {description && <span className="cat-card-desc">{description}</span>}
      </span>
    </Link>
  );
}

function VonkDocCard({ item }) {
  switch (item.type) {
    case 'link':
      return <CardLink item={item} />;
    case 'category':
      return <CardCategory item={item} />;
    default:
      throw new Error(`unknown item type ${JSON.stringify(item)}`);
  }
}

export default function DocCard(props) {
  const { pathname } = useLocation();
  return pathname.includes('/VonkUltra/') ? (
    <VonkDocCard {...props} />
  ) : (
    <OriginalDocCard {...props} />
  );
}
