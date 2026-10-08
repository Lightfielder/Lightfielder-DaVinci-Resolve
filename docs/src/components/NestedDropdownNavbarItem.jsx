import React, {useState} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';

/**
 * A navbar item that renders a clickable root link plus a dropdown whose items
 * may contain nested groups. Nested groups expand INLINE, downward within the
 * same dropdown column (accordion style) — they do not fly out to the right.
 *
 * Docusaurus forbids nested `dropdown` items in config, so this custom
 * `custom-nestedDropdown` item provides that capability.
 *
 * Config shape:
 *   {
 *     type: 'custom-nestedDropdown',
 *     label: 'Resolve/Fusion',
 *     to: '/docs/',                 // root link (clickable)
 *     items: [
 *       { label: 'Overview', to: '/docs/' },
 *       { label: 'Installation', items: [ { label: 'Install Lightfielder', to: '...' }, ... ] },
 *     ],
 *   }
 */

function isExternal(href) {
  return typeof href === 'string' && /^https?:\/\//.test(href);
}

function ItemLink({item, className, onClick}) {
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
      {...(isExternal(item.href) ? {target: '_blank', rel: 'noopener noreferrer'} : {})}>
      {item.label}
    </a>
  );
}

function Leaf({item}) {
  return (
    <li>
      <ItemLink item={item} className="dropdown__link" />
    </li>
  );
}

function Group({item}) {
  const [open, setOpen] = useState(false);
  return (
    <li className="lf-group">
      <button
        type="button"
        className="lf-group__toggle"
        aria-expanded={open}
        onClick={() => setOpen((o) => !o)}>
        <span className="lf-group__label">{item.label}</span>
        <span className="lf-group__caret" aria-hidden="true">
          {open ? '▾' : '▸'}
        </span>
      </button>
      {open && (
        <ul className="lf-group__menu">
          {item.items.map((child, i) => (
            <Node item={child} key={i} />
          ))}
        </ul>
      )}
    </li>
  );
}

function Node({item}) {
  return Array.isArray(item.items) && item.items.length > 0 ? (
    <Group item={item} />
  ) : (
    <Leaf item={item} />
  );
}

function MobileNode({item, onClick}) {
  const hasChildren = Array.isArray(item.items) && item.items.length > 0;
  return (
    <li className="menu__list-item">
      <ItemLink item={item} className="menu__link" mobile onClick={onClick} />
      {hasChildren && (
        <ul className="menu__list">
          {item.items.map((child, i) => (
            <MobileNode item={child} key={i} onClick={onClick} />
          ))}
        </ul>
      )}
    </li>
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
  const rootItem = {label, to, href};

  if (mobile) {
    return (
      <li className={clsx('menu__list-item', className)}>
        <ItemLink item={rootItem} className="menu__link" mobile onClick={onClick} />
        {items.length > 0 && (
          <ul className="menu__list">
            {items.map((item, i) => (
              <MobileNode item={item} key={i} onClick={onClick} />
            ))}
          </ul>
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
      <ul className="dropdown__menu">
        {items.map((item, i) => (
          <Node item={item} key={i} />
        ))}
      </ul>
    </div>
  );
}
