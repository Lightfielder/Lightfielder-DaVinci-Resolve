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
            type: 'doc',
            docId: 'index',
            position: 'left',
            label: 'Docs',
          },
          {
            to: '/docs/usage/toolbar',
            position: 'left',
            label: 'Toolbar',
          },
          {
            to: '/docs/workflow-guides/',
            position: 'left',
            label: 'Guides',
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
                label: 'Lightfielder Ops',
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
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
