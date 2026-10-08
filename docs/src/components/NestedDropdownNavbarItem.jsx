import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';

/**
 * A navbar item that renders a clickable root link plus a dropdown whose items
 * may themselves contain nested items (sub-sub fold-outs). Docusaurus forbids
 * nested `dropdown` items in config, so this custom `custom-nestedDropdown`
 * item provides that capability.
 *
 * Config shape:
 *   {
 *     type: 'custom-nestedDropdown',
 *     label: 'Toolbar',
 *     to: '/docs/usage/toolbar',        // root link (clickable)
 *     items: [
 *       { label: 'Overview', to: '/docs/usage/toolbar' },
 *       {
 *         label: 'Toolbar Scripts',
 *         to: '/docs/category/toolbar-scripts',
 *         items: [ { label: '00 Toolbar', to: '/docs/usage/scripts/toolbar' }, ... ],
 *       },
 *     ],
 *   }
 */

function isExternal(href) {
  return typeof href === 'string' && /^https?:\/\//.test(href);
}

function ItemLink({ item, className, mobile, onClick }) {
  if (item.to) {
    return (
      <Link className={className} to={item.to} onClick={onClick}>
        {item.label}
      </Link>
    );
  }
  return (
    <a
      className={className}
      href={item.href}
      onClick={onClick}
      {...(isExternal(item.href) ? { target: '_blank', rel: 'noopener noreferrer' } : {})}>
      {item.label}
    </a>
  );
}

function DesktopItems({ items, nested }) {
  return (
    <ul className={nested ? 'lf-submenu__menu' : 'dropdown__menu'}>
      {items.map((item, i) => {
        const hasChildren = Array.isArray(item.items) && item.items.length > 0;
        if (hasChildren) {
          return (
            <li className="lf-submenu" key={i}>
              <span className="lf-submenu__row">
                <ItemLink item={item} className="dropdown__link lf-submenu__link" />
                <span className="lf-submenu__caret" aria-hidden="true">
                  ›
                </span>
              </span>
              <DesktopItems items={item.items} nested />
            </li>
          );
        }
        return (
          <li key={i}>
            <ItemLink item={item} className="dropdown__link" />
          </li>
        );
      })}
    </ul>
  );
}

function MobileItems({ items, nested, onClick }) {
  return (
    <ul className="menu__list">
      {items.map((item, i) => {
        const hasChildren = Array.isArray(item.items) && item.items.length > 0;
        return (
          <li className="menu__list-item" key={i}>
            <ItemLink
              item={item}
              className="menu__link"
              mobile
              onClick={onClick}
            />
            {hasChildren && (
              <MobileItems items={item.items} nested onClick={onClick} />
            )}
          </li>
        );
      })}
    </ul>
  );
}

export default function NestedDropdownNavbarItem({
  label,
  to,
  href,
  items = [],
  position,
  mobile,
  onClick,
  className,
  ...rest
}) {
  const rootItem = { label, to, href };

  if (mobile) {
    return (
      <li className={clsx('menu__list-item', className)}>
        <ItemLink item={rootItem} className="menu__link" mobile onClick={onClick} />
        {items.length > 0 && (
          <MobileItems items={items} onClick={onClick} />
        )}
      </li>
    );
  }

  return (
    <div
      className={clsx(
        'navbar__item',
        'dropdown',
        'dropdown--hoverable',
        'lf-nested-dropdown',
        {'dropdown--right': position === 'right'},
        className
      )}
      {...rest}>
      <ItemLink item={rootItem} className="navbar__link" />
      <DesktopItems items={items} />
    </div>
  );
}
