import React from 'react';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { TYPE_CONFIG } from '@site/src/data/categoryConfig';
import { MOG_COUNTS, CORE_COUNTS, sum, TOTAL, DATA_TYPE_COUNT } from '@site/src/data/homepageCounts';
import styles from '@site/src/css/homepage.module.css';

/**
 * Kartaverse Vonk Ultra landing content.
 *
 * Ported from the standalone Vonk Ultra docs homepage (src/pages/index.js) so
 * the /VonkUltra/ landing page reads the same, but adapted to render inside a
 * docs page: no full-page <Layout>, baseUrl-aware icon URLs, and every link
 * rewritten from /docs/... to /VonkUltra/...
 */

const PILLARS = [
  {
    num: '01',
    eyebrow: 'Fundamentals',
    title: 'Introduction',
    desc: 'How typed data moves between nodes, and when to reach for Mograph versus Core.',
    cta: 'Read the introduction →',
    to: '/VonkUltra/getting-started/introduction',
  },
  {
    num: '02',
    eyebrow: 'Package Deployment',
    title: 'Install via Reactor',
    desc: 'Free and open source (GPL-3.0), distributed through the Reactor Package Manager for Fusion Studio and DaVinci Resolve.',
    cta: 'Install instructions →',
    to: '/VonkUltra/getting-started/install',
  },
  {
    num: '03',
    eyebrow: 'Mastery Workflows',
    title: 'Interactive Tutorials',
    desc: 'Video walkthroughs, comp and tool scripts, and worked examples you can pull apart.',
    cta: 'Browse tutorials →',
    to: '/VonkUltra/tutorials/video-tutorials',
  },
];

const CENTER = 160;
const RINGS = [
  { r: 150, count: 6, offset: 0 },
  { r: 105, count: 6, offset: 30 },
  { r: 58, count: 6, offset: 15 },
];

const polar = (r, deg) => {
  const a = ((deg - 90) * Math.PI) / 180;
  return [CENTER + r * Math.cos(a), CENTER + r * Math.sin(a)];
};

function NodeDiagram() {
  return (
    <svg viewBox="0 0 320 320" className={styles.diagram} role="img"
         aria-label="Schematic of nodes connected in a graph">
      {RINGS.map(({ r }) => (
        <circle key={r} cx={CENTER} cy={CENTER} r={r} fill="none"
                stroke="currentColor" strokeWidth="1"
                strokeDasharray={r === 105 ? '3 5' : undefined} />
      ))}
      {RINGS.map(({ r, count, offset }) =>
        Array.from({ length: count }, (_, i) => {
          const [x, y] = polar(r, (360 / count) * i + offset);
          return (
            <g key={`${r}-${i}`}>
              <line x1={CENTER} y1={CENTER} x2={x} y2={y} stroke="currentColor" strokeWidth="0.6" />
              <rect x={x - 3} y={y - 3} width="6" height="6" fill="currentColor" />
            </g>
          );
        })
      )}
      <circle cx={CENTER} cy={CENTER} r="4" fill="currentColor" />
    </svg>
  );
}

const RAMP_FROM = [255, 203, 107]; // --lf-gold
const RAMP_TO = [58, 45, 18]; //      deep bronze
const RAMP_ALPHA = 0.3;

function rampShade(i, total) {
  const t = total <= 1 ? 0 : i / (total - 1);
  const rgb = RAMP_FROM.map((v, k) => Math.round(v + (RAMP_TO[k] - v) * t));
  return `rgb(${rgb.join(' ')} / ${RAMP_ALPHA})`;
}

function TypeCard({ name, count, base, shade }) {
  const cfg = TYPE_CONFIG[name] || {};
  const family = base.charAt(0).toUpperCase() + base.slice(1);
  const iconUrl = useBaseUrl(`/img/vonkultra/icons/${family}_${name}.svg`);
  return (
    <Link className="cat-card" to={`/VonkUltra/reference/${base}/${name.toLowerCase()}/`}>
      <span
        className={`cat-card-icon cat-card-icon--${cfg.color || 'default'}`}
        style={{'--cat-card-icon-bg': shade}}>
        <span
          className="cat-card-icon-glyph"
          style={{'--cat-card-icon': `url("${iconUrl}")`}}
        />
      </span>
      <span className="cat-card-body">
        <span className="cat-card-title">
          {name}
          <span className="cat-card-count">
            {count} node{count === 1 ? '' : 's'}
          </span>
        </span>
        {cfg.desc && <span className="cat-card-desc">{cfg.desc}</span>}
      </span>
    </Link>
  );
}

function Family({ id, title, count, counts, base, blurb, shadeOffset }) {
  return (
    <section id={id} style={{ marginBottom: '2.5rem' }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.75rem', flexWrap: 'wrap' }}>
        <Heading as="h3" style={{ margin: 0 }}>{title}</Heading>
        <span className={styles.mono} style={{ opacity: 0.7, fontSize: '0.75rem' }}>{count} nodes</span>
      </div>
      <p style={{ opacity: 0.8, marginBottom: '0.5rem' }}>{blurb}</p>
      <div className={styles.grid3}>
        {Object.entries(counts).map(([name, c], i) => (
          <TypeCard key={name} name={name} count={c} base={base}
                    shade={rampShade(shadeOffset + i, DATA_TYPE_COUNT)} />
        ))}
      </div>
    </section>
  );
}

export default function VonkUltraHome() {
  return (
    <>
      <header className={styles.hero2}>
        <div>
          <div className={styles.badgeWrap}>
            <span className={styles.badge}>
              <span className={styles.liveDot} />
              <span className={styles.accent}>GPL-3.0</span>
              <span className={styles.badgeSep}>•</span>
              <span>Blackmagic Fusion 18–21.1</span>
              <span className={styles.badgeSep}>•</span>
              <span>Resolve Studio &amp; Free</span>
            </span>
          </div>
          <Heading as="h1" className={styles.hero2Title}>
            <span className="brand-gold">Kartaverse</span>{' '}
            <span className="brand-plain">Vonk Ultra</span>
          </Heading>
          <p className={styles.hero2Sub}>A new era of no-code creativity inside Blackmagic Fusion.</p>
          <p className={styles.hero2Lead}>
            Connect Array, JSON, Matrix and Text nodes to build data-driven
            motion graphics — no scripting required. Runs inside DaVinci Resolve
            Studio and standalone Fusion.
          </p>
          <div className={styles.btnRow}>
            <Link className="button button--primary button--lg" to="/VonkUltra/getting-started/introduction">
              Get Started
            </Link>
            <Link className="button button--secondary button--lg" to="/VonkUltra/getting-started/install">
              Install (Reactor)
            </Link>
          </div>
        </div>
        <NodeDiagram />
      </header>

      <div className={styles.navRow}>
        {PILLARS.map((p) => (
          <Link key={p.num} className={styles.navCard} to={p.to}>
            <span className={styles.pillarNum}>{p.num}</span>
            <span className={styles.eyebrow}>{p.eyebrow}</span>
            <span className={styles.navTitle}>{p.title}</span>
            <p className={styles.navDesc}>{p.desc}</p>
            <span className={styles.pillarCta}>{p.cta}</span>
          </Link>
        ))}
      </div>

      <Heading as="h2">Browse the Reference</Heading>
      <p style={{ opacity: 0.8, margin: 0 }}>
        {TOTAL} documented nodes across {DATA_TYPE_COUNT} data types — one unified
        specification per node.
      </p>
      <div className={styles.filters}>
        <a className={`${styles.pill} ${styles.pillActive}`} href="#reference">All ({TOTAL})</a>
        <a className={styles.pill} href="#mograph">Mograph ({sum(MOG_COUNTS)})</a>
        <a className={styles.pill} href="#core">Core ({sum(CORE_COUNTS)})</a>
      </div>

      <div id="reference" style={{ marginTop: '2.5rem' }}>
        <Family id="mograph" title="Mograph" count={sum(MOG_COUNTS)} counts={MOG_COUNTS}
                base="mograph" blurb="Purpose-built for motion graphics pipelines."
                shadeOffset={0} />
        <Family id="core" title="Core" count={sum(CORE_COUNTS)} counts={CORE_COUNTS}
                base="core" blurb="The general-purpose toolset — data types, files, text, images and more."
                shadeOffset={Object.keys(MOG_COUNTS).length} />
      </div>
    </>
  );
}
