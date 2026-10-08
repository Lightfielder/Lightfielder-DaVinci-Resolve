// Lightfielder for DaVinci Resolve — Docusaurus configuration.
//
// The site scaffolding, theme, and plugin lineup are ported/inspired by the
// VFXPedia docs project (https://github.com/Lightfielder/VFXPedia) so the
// Lightfielder help docs read as part of the same design family:
// IBM Plex typography, indigo light theme, deep blue-black + gold dark theme,
// Mermaid diagram support, and self-contained local full-text search.

const prism = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
module.exports = {
  title: 'Lightfielder for DaVinci Resolve',
  tagline: 'Multi-view workflow automation for volumetric post-production',
  url: 'https://lightfielder.github.io',
  baseUrl: '/Lightfielder-DaVinci-Resolve/',
  onBrokenLinks: 'warn',
  favicon: 'img/favicon.svg',

  organizationName: 'Lightfielder',
  projectName: 'Lightfielder-DaVinci-Resolve',

  // Google Fonts: IBM Plex Sans for headings + body, IBM Plex Mono for code,
  // tables, counts and labels. Shared with the VFXPedia and Swiftpedia docs
  // sites so the projects read as one design family.
  stylesheets: [
    {
      href: 'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap',
      type: 'text/css',
    },
  ],

  // Mermaid theme for rendering diagrams inside the docs.
  themes: [
    '@docusaurus/theme-mermaid',
    // Site-wide full-text search, self-contained (no external account).
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        language: ['en'],
        indexBlog: false,
        // Index both documentation instances: the Lightfielder docs (default
        // `docs` route) and the imported Vonk Ultra reference (/VonkUltra/).
        docsRouteBasePath: ['docs', 'VonkUltra'],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
      },
    ],
  ],

  // Markdown configuration.
  markdown: {
    // Parse .md files as CommonMark (MDX only for .mdx files) so the existing
    // help topics can use inline HTML, email autolinks, and angle brackets.
    format: 'detect',
    mermaid: true,
    hooks: {
      onBrokenMarkdownImages: () => {
        // Ignore broken markdown image errors.
        return;
      },
      onBrokenMarkdownLinks: 'warn',
    },
  },

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Follow the OS light/dark preference on first visit.
      colorMode: {
        respectPrefersColorScheme: true,
      },
      mermaid: {
        theme: {
          light: 'default',
          dark: 'dark',
        },
        options: {
          flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'linear',
            padding: 8,
            nodeSpacing: 40,
            rankSpacing: 50,
          },
        },
      },
      navbar: {
        title: 'Lightfielder',
        logo: {
          alt: 'Lightfielder logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'custom-nestedDropdown',
            label: 'Resolve/Fusion',
            position: 'left',
            to: '/docs/',
            items: [
              { label: 'Overview', to: '/docs/' },
              {
                label: 'Installation',
                to: '/docs/category/installation',
                items: [
                  { label: 'Install Lightfielder', to: '/docs/installation/install-lightfielder' },
                  { label: 'Install Python', to: '/docs/installation/install-python' },
                  { label: 'Uninstall Lightfielder', to: '/docs/installation/uninstall-lightfielder' },
                ],
              },
              {
                label: 'Usage',
                to: '/docs/category/usage',
                items: [
                  { label: 'Toolbar Scripts', to: '/docs/usage/toolbar' },
                  { label: 'Metadata Tags', to: '/docs/usage/metadata-tags' },
                  { label: 'Shotlog Format', to: '/docs/usage/shotlog' },
                  { label: 'Deliver Page Presets', to: '/docs/usage/deliver-page-presets' },
                  { label: 'Unit Tests', to: '/docs/usage/unit-tests' },
                ],
              },
              {
                label: 'Workflow Guides',
                to: '/docs/workflow-guides/',
                items: [
                  { label: 'Guides Overview', to: '/docs/workflow-guides/' },
                  { label: 'Live Grade Video Flowchart', to: '/docs/workflow-guides/lightfielder-live-grade-flowchart' },
                  { label: 'HDR Image Based Rendering', to: '/docs/workflow-guides/lightfielder-hdr-image-based-rendering' },
                  { label: 'Volumetric Color Decision Lists', to: '/docs/workflow-guides/volumetric-color-decision-lists' },
                  { label: 'PBR-GS Gaussian Splats', to: '/docs/workflow-guides/physically-based-rendering-of-gaussian-splats' },
                  { label: 'The OBJ-GS Guide', to: '/docs/workflow-guides/obj-gs' },
                ],
              },
              {
                label: 'Editorial/Grading Project',
                to: '/docs/category/project',
                items: [
                  { label: 'ChangeLog', to: '/docs/project/changelog' },
                  { label: 'Known Issues', to: '/docs/project/known-issues' },
                  { label: 'PunchList', to: '/docs/project/punch-list' },
                ],
              },
              {
                label: 'Examples',
                to: '/docs/Examples/',
                items: [
                  { label: 'Example Projects', to: '/docs/Examples/' },
                  { label: 'Pikachu Still Frame 50 View', to: '/docs/Examples/pikachu-still-frame-50-view' },
                ],
              },
            ],
          },
          {
            type: 'custom-nestedDropdown',
            label: 'Toolbar',
            position: 'left',
            to: '/docs/usage/toolbar',
            items: [
              { label: 'Toolbar Overview', to: '/docs/usage/toolbar' },
              {
                label: 'Toolbar Scripts',
                to: '/docs/category/toolbar-scripts',
                items: [
                  { label: '00 Toolbar', to: '/docs/usage/scripts/toolbar' },
                  { label: '01 Preferences', to: '/docs/usage/scripts/preferences' },
                  { label: '02 Bin Templates', to: '/docs/usage/scripts/bin-templates' },
                  { label: '03 Shotlog Pre-Flight', to: '/docs/usage/scripts/shotlog-preflight' },
                  { label: '04 Import Footage', to: '/docs/usage/scripts/import-footage' },
                  { label: '05 Metadata Sync', to: '/docs/usage/scripts/metadata-sync' },
                  { label: '06 Still Frames Export', to: '/docs/usage/scripts/still-frames-export' },
                  { label: '07 Create EDLs', to: '/docs/usage/scripts/create-edls' },
                  { label: '08 Batch Trim', to: '/docs/usage/scripts/batch-trim' },
                  { label: '09 EDL Stack Swizzle', to: '/docs/usage/scripts/edl-stack-swizzle' },
                  { label: '10 EDL Checker', to: '/docs/usage/scripts/edl-checker' },
                  { label: '11 Log Viewer', to: '/docs/usage/scripts/log-viewer' },
                  { label: '12 Video Track Solo', to: '/docs/usage/scripts/video-track-solo' },
                  { label: '13 Camera Contact Sheet', to: '/docs/usage/scripts/camera-contact-sheet' },
                  { label: '14 Grade Automation', to: '/docs/usage/scripts/grade-automation' },
                  { label: '15 EDL Export', to: '/docs/usage/scripts/edl-export' },
                  { label: '16 Extensions', to: '/docs/usage/scripts/extensions' },
                  { label: '17 Edit Jupyter Link', to: '/docs/usage/scripts/jupyter-link' },
                  { label: '18 Media Command', to: '/docs/usage/scripts/media-command' },
                  { label: '19 Edit Python Module', to: '/docs/usage/scripts/edit-python-module' },
                  { label: '20 Show Console', to: '/docs/usage/scripts/show-console' },
                  { label: '21 Documentation', to: '/docs/usage/scripts/documentation' },
                  { label: '22 About Lightfielder', to: '/docs/usage/scripts/about-lightfielder' },
                  { label: 'Open Lightfielder Folder', to: '/docs/usage/scripts/open-lightfielder-folder' },
                ],
              },
            ],
          },
          {
            type: 'dropdown',
            label: 'Guides',
            position: 'left',
            to: '/docs/workflow-guides/',
            items: [
              { label: 'Guides Overview', to: '/docs/workflow-guides/' },
              { label: 'Live Grade Video Flowchart', to: '/docs/workflow-guides/lightfielder-live-grade-flowchart' },
              { label: 'HDR Image Based Rendering', to: '/docs/workflow-guides/lightfielder-hdr-image-based-rendering' },
              { label: 'Volumetric Color Decision Lists', to: '/docs/workflow-guides/volumetric-color-decision-lists' },
              { label: 'PBR-GS Gaussian Splats', to: '/docs/workflow-guides/physically-based-rendering-of-gaussian-splats' },
              { label: 'The OBJ-GS Guide', to: '/docs/workflow-guides/obj-gs' },
            ],
          },
          {
            type: 'dropdown',
            label: 'Ops',
            position: 'left',
            to: '/docs/Ops/',
            items: [
              { label: 'Ops Overview', to: '/docs/Ops/' },
              { label: 'Install Ops', to: '/docs/Ops/installation/install-ops' },
              { label: 'Install Python', to: '/docs/Ops/installation/install-python' },
              { label: 'Uninstall Ops', to: '/docs/Ops/installation/uninstall-ops' },
              { label: 'Sequencer View', to: '/docs/Ops/usage/sequencer' },
              { label: 'Nodes View', to: '/docs/Ops/usage/nodes' },
              { label: 'Export Presets', to: '/docs/Ops/usage/presets' },
              { label: 'Unit Tests', to: '/docs/Ops/usage/unit-tests' },
              { label: 'Lightfielder Viewport', to: '/docs/Ops/viewport/' },
            ],
          },
          {
            type: 'dropdown',
            label: 'Examples',
            position: 'left',
            to: '/docs/Examples/',
            items: [
              { label: 'Examples Overview', to: '/docs/Examples/' },
              { label: 'Pikachu Still Frame 50 View', to: '/docs/Examples/pikachu-still-frame-50-view' },
            ],
          },
          {
            type: 'dropdown',
            label: 'Vonk Ultra',
            position: 'left',
            to: '/VonkUltra/',
            items: [
              { label: 'Overview', to: '/VonkUltra/' },
              { label: 'Getting Started', to: '/VonkUltra/getting-started/introduction' },
              { label: 'Reference', to: '/VonkUltra/reference' },
              { label: 'Guides', to: '/VonkUltra/guides/overview' },
              { label: 'Tutorials', to: '/VonkUltra/tutorials/video-tutorials' },
            ],
          },
          {
            href: 'https://medium.com/@andrewhazelden',
            label: 'Blog',
            position: 'right',
          },
          {
            href: 'https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentation',
            items: [
              { label: 'Overview', to: '/docs/' },
              { label: 'Installation', to: '/docs/installation/install-lightfielder' },
              { label: 'Toolbar Scripts', to: '/docs/usage/toolbar' },
              { label: 'Workflow Guides', to: '/docs/workflow-guides/' },
              { label: 'Lightfielder Ops', to: '/docs/Ops/' },
              { label: 'Vonk Ultra', to: '/VonkUltra/' },
            ],
          },
          {
            title: 'Project',
            items: [
              { label: 'ChangeLog', to: '/docs/project/changelog' },
              { label: 'Known Issues', to: '/docs/project/known-issues' },
              { label: 'PunchList', to: '/docs/project/punch-list' },
              { label: 'Unit Tests', to: '/docs/usage/unit-tests' },
            ],
          },
          {
            title: 'Links',
            items: [
              {
                label: 'Blog',
                href: 'https://medium.com/@andrewhazelden',
              },
              {
                label: 'GitHub Repository',
                href: 'https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve',
              },
              {
                label: 'Releases',
                href: 'https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve/releases',
              },
              {
                label: 'Lightfielder Ops Repo',
                href: 'https://github.com/Lightfielder/LightfielderOperators',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Lightfielder. Built with Docusaurus.`,
      },
      prism: {
        theme: prism.themes.github,
        darkTheme: prism.themes.dracula,
        // The Lightfielder docs share Python, Lua, Bash and JSON snippets.
        additionalLanguages: ['lua', 'bash', 'python', 'json'],
      },
    }),

  // Imported Kartaverse Vonk Ultra documentation site. It runs as a second,
  // independent docs plugin instance so its four original sidebars and ~1000
  // node reference pages stay separate from the Lightfielder docs, and it is
  // served under the /VonkUltra/ route.
  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'vonkultra',
        path: 'vonkultra',
        routeBasePath: 'VonkUltra',
        sidebarPath: require.resolve('./sidebarsVonkUltra.js'),
      },
    ],
  ],

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/Lightfielder/Lightfielder-DaVinci-Resolve/tree/main/docs/docs/',
        },
        blog: false,
        theme: {
          customCss: [
            require.resolve('./src/css/custom.css'),
            require.resolve('./src/css/vonkultra.css'),
            require.resolve('./src/css/examples.css'),
            require.resolve('./src/css/navbar.css'),
          ],
        },
      },
    ],
  ],
};
