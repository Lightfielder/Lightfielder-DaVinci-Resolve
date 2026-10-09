import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';

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

/**
 * Polar "ray" motif for the landing page hero.
 *
 * Ported from the Kartaverse Vonk Ultra docs site (src/pages/index.js
 * NodeDiagram). It draws concentric rings with radial rays connecting the
 * centre to node points placed with polar coordinates — a lightfield / camera
 * array style graphic that suits the Lightfielder theme.
 */
function NodeDiagram() {
  return (
    <svg
      viewBox="0 0 320 320"
      className="lf-diagram"
      role="img"
      aria-label="Polar diagram of camera array rays radiating from a central point">
      {RINGS.map(({ r }) => (
        <circle
          key={r}
          cx={CENTER}
          cy={CENTER}
          r={r}
          fill="none"
          stroke="currentColor"
          strokeWidth="1"
          strokeDasharray={r === 105 ? '3 5' : undefined}
        />
      ))}
      {RINGS.map(({ r, count, offset }) =>
        Array.from({ length: count }, (_, i) => {
          const [x, y] = polar(r, (360 / count) * i + offset);
          return (
            <g key={`${r}-${i}`}>
              <line
                x1={CENTER}
                y1={CENTER}
                x2={x}
                y2={y}
                stroke="currentColor"
                strokeWidth="0.6"
              />
              <rect x={x - 3} y={y - 3} width="6" height="6" fill="currentColor" />
            </g>
          );
        })
      )}
      <circle cx={CENTER} cy={CENTER} r="4" fill="currentColor" />
    </svg>
  );
}

const sections = [
  {
    title: 'Getting Started',
    links: [
      { label: 'Overview', href: '/docs/' },
      { label: 'Install Lightfielder', href: '/docs/installation/install-lightfielder' },
      { label: 'Install Python', href: '/docs/installation/install-python' },
      { label: 'Uninstall Lightfielder', href: '/docs/installation/uninstall-lightfielder' },
    ],
  },
  {
    title: 'Toolbar scripts',
    links: [
      { label: 'Toolbar Overview', href: '/docs/usage/toolbar' },
      { label: '00 Toolbar', href: '/docs/usage/scripts/toolbar' },
      { label: '01 Preferences', href: '/docs/usage/scripts/preferences' },
      { label: '02 Bin Templates', href: '/docs/usage/scripts/bin-templates' },
      { label: '03 Shotlog Pre-Flight', href: '/docs/usage/scripts/shotlog-preflight' },
      { label: '04 Import Footage', href: '/docs/usage/scripts/import-footage' },
      { label: '05 Metadata Sync', href: '/docs/usage/scripts/metadata-sync' },
      { label: 'Show more', href: '/docs/category/toolbar-scripts' },
    ],
  },
  {
    title: 'LF Stand & Deliver',
    links: [
      { label: 'Metadata Tags', href: '/docs/usage/metadata-tags' },
      { label: 'Shotlog Format', href: '/docs/usage/shotlog' },
      { label: 'Deliver Page Presets', href: '/docs/usage/deliver-page-presets' },
      { label: 'Unit Tests', href: '/docs/usage/unit-tests' },
    ],
  },
  {
    title: 'Workflow Guides',
    links: [
      { label: 'Live Grade Video Flowchart', href: '/docs/workflow-guides/lightfielder-live-grade-flowchart' },
      { label: 'HDR Image Based Rendering', href: '/docs/workflow-guides/lightfielder-hdr-image-based-rendering' },
      { label: 'Volumetric Color Decision Lists', href: '/docs/workflow-guides/volumetric-color-decision-lists' },
      { label: 'PBR-GS Gaussian Splats', href: '/docs/workflow-guides/physically-based-rendering-of-gaussian-splats' },
      { label: 'The OBJ-GS Guide', href: '/docs/workflow-guides/obj-gs' },
    ],
  },
  {
    title: 'Lightfielder Ops',
    links: [
      { label: 'Ops Overview', href: '/docs/Ops/' },
      { label: 'Install Ops', href: '/docs/Ops/installation/install-ops' },
      { label: 'Sequencer View', href: '/docs/Ops/usage/sequencer' },
      { label: 'Nodes View', href: '/docs/Ops/usage/nodes' },
      { label: 'Lightfielder Viewport', href: '/docs/Ops/viewport/' },
    ],
  },
  {
    title: 'Vonk Ultra',
    links: [
      { label: 'Overview', href: '/VonkUltra/' },
      { label: 'Getting Started', href: '/VonkUltra/getting-started/introduction' },
      { label: 'Reference', href: '/VonkUltra/reference' },
      { label: 'Guides', href: '/VonkUltra/guides/overview' },
      { label: 'Tutorials', href: '/VonkUltra/tutorials/video-tutorials' },
    ],
  },
  {
    title: 'Lightfield Example Projects',
    links: [
      { label: 'Example Projects', href: '/docs/Examples/' },
      { label: 'Pikachu Still Frame 50 View', href: '/docs/Examples/pikachu-still-frame-50-view' },
    ],
  },
  {
    title: 'LF for Resolve',
    links: [
      { label: 'ChangeLog', href: '/docs/project/changelog' },
      { label: 'Known Issues', href: '/docs/project/known-issues' },
      { label: 'PunchList', href: '/docs/project/punch-list' },
    ],
  },
  {
    title: 'External Resources',
    links: [
      { label: 'GitHub Repository', href: 'https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve' },
      { label: 'GitHub Releases', href: 'https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve/releases' },
      { label: 'Lightfielder Ops', href: 'https://github.com/Lightfielder/LightfielderOperators' },
      { label: 'VFXPedia Docs Site', href: 'https://lightfielder.github.io/VFXPedia/' },
      { label: 'Swiftpedia Docs Site', href: 'https://github.com/Lightfielder/Swiftpedia' },
      { label: 'Maya Camera Snap', href: 'https://github.com/Lightfielder/Maya-CameraSnap-Tools' },
      { label: 'Kartaverse for Houdini', href: 'https://kartaverse.github.io/Kartaverse-for-Houdini/' },
    ],
  },
];

export default function Home() {
  return (
    <Layout
      title="Lightfielder for DaVinci Resolve"
      description="Multi-view workflow automation for volumetric post-production">
      <main className="lf-main-page">
        <header className="lf-hero">
          <div className="lf-hero-grid">
            <div className="lf-hero-copy">
              <span className="lf-badge">Blackmagic DaVinci Resolve · Multi-View</span>
              <Heading as="h1" className="lf-hero-title">
                <span className="brand-gold">Light</span>
                <span className="brand-plain">fielder</span>
              </Heading>
              <p className="lf-hero-sub">
                Multi-view workflow automation for volumetric post-production
              </p>
              <div className="lf-btn-row">
                <Link className="button button--primary button--lg" to="/docs/">
                  Read the Docs
                </Link>
                <a
                  className="button button--secondary button--lg"
                  href="https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve/releases"
                  target="_blank"
                  rel="noopener noreferrer">
                  Download
                </a>
                <Link className="button button--secondary button--lg lf-btn-row__full" to="/docs/installation/install-lightfielder">
                  Install Lightfielder
                </Link>
              </div>
            </div>
            <NodeDiagram />
          </div>
        </header>
        <section className="lf-note">
          <Heading as="h2">What does this software do?</Heading>
          <p>
            Lightfielder (aka "LF") is an LGPL-licensed open-source hybrid computer-vision IDE
            and digital content creation (DCC) toolset developed by Andrew Hazelden.
            Designed to unify volumetric video content creation and XR
            post-production. The current  Lightfielder public beta release cycle is aimed at a professional
            audience that is already working in the 3D graphics and immersive media
            sector.
					</p>
          <p>
						The goal with Lightfielder v26 is to gather feedback from the community so we can help
            shape the future of accessible, high-performance, open-source multi-view
            pipelines. This is part of the process of taking Lightfielder from its status as an in-house tool created between 2022-2026, and spinning it out for wider public access. This will involve further refinement of the user interface and adding more flexible camera rig design support via "user defined" Python plug-ins that can be dropped into the pipeline.
          </p>
        </section>
        <div className="lf-sections-grid">
          {sections.map((section, idx) => (
            <div key={idx} className="lf-section-card">
              <h3 className="lf-section-title">{section.title}</h3>
              <ul className="lf-section-links">
                {section.links.map((link, i) => (
                  <li key={i}>
                    {link.href.startsWith('http') ? (
                      <a href={link.href} target="_blank" rel="noopener noreferrer">{link.label}</a>
                    ) : (
                      <Link to={link.href}>{link.label}</Link>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <section className="lf-about">
          <Heading as="h2">Am I Lightfielder?</Heading>
          <p>
            You might be. Are you a tech artist, photographer, or filmmaker working
            with multi-view content in the plenoptic imaging domain? Do you
            frequently capture or process lightfield data? If YES, then you can
            easily use the colloquial term &quot;Lightfielder&quot; to describe your
            craft.
          </p>

          <Heading as="h2">What is a Lightfield Capture of a Scene?</Heading>
          <p>
            Lightfield recordings of a real-world or virtual scene provide a unique
            experience compared to traditional legacy VR/XR media types (like 360VR,
            180VR, Fulldome, 3DTV, or Spatial Media).
          </p>
          <p>
            When digitized, a lightfield based 3D scene-graph stores the captured
            content using a data structure that holds the individual samples of
            light rays. Each ray has a unique light intensity property and a light
            ray direction property that indicates the angle that the light beam is
            travelling along.
          </p>
          <p>
            This allows the observer of a lightfield scene asset to experience
            free-view motion (aka 6DoF navigation) when viewing the digital
            environment. The observer is able to interactively re-adjust the
            synthetic camera properties such as aperture, exposure, colour
            temperature, and shutter angle to sculpt the final cinematic result. A
            lightfield photography/filmmaking approach can be used to display a
            still representation of a scene (freezing a single moment in time), or a
            full motion version of the scene which supports narrative storytelling
            goals.
          </p>
        </section>
      </main>
    </Layout>
  );
}