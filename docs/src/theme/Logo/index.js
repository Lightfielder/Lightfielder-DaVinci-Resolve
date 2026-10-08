import React from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {useThemeConfig} from '@docusaurus/theme-common';
import ThemedImage from '@theme/ThemedImage';

/**
 * Swizzled @theme/Logo.
 *
 * Ported from the VFXPedia docs site. The brand wordmark is split into two
 * tones: the leading "Light" takes the shared brand gold, the "fielder" suffix
 * keeps the default ink colour — echoing VFXPedia's two-tone "VFX" + "pedia"
 * brand treatment so the sites are recognisably the same design family.
 *
 * Upstream source: @docusaurus/theme-classic/lib/theme/Logo/index.js
 */

function LogoThemedImage({logo, alt, imageClassName}) {
  const sources = {
    light: useBaseUrl(logo.src),
    dark: useBaseUrl(logo.srcDark || logo.src),
  };
  const themedImage = (
    <ThemedImage
      className={logo.className}
      sources={sources}
      height={logo.height}
      width={logo.width}
      alt={alt}
      style={logo.style}
    />
  );
  return imageClassName ? (
    <div className={imageClassName}>{themedImage}</div>
  ) : (
    themedImage
  );
}

function BrandTitle({title, className}) {
  // "Lightfielder" is a single-word wordmark, so split the leading "Light"
  // from the rest to get a two-tone effect. Fall back to splitting on a space
  // for titles like "Lightfielder for DaVinci Resolve".
  const match = title.match(/^(Light)(fielder.*)$/i);
  const first = match ? match[1] : title.split(' ')[0];
  const rest = match ? match[2] : title.split(' ').slice(1).join(' ');
  const remainder = match || !rest ? rest : ` ${rest}`;
  return (
    <b className={className}>
      <span className="brand-gold">{first}</span>
      {remainder ? <span className="brand-plain">{remainder}</span> : ''}
    </b>
  );
}

export default function Logo(props) {
  const {
    siteConfig: {title},
  } = useDocusaurusContext();
  const {
    navbar: {title: navbarTitle, logo},
  } = useThemeConfig();
  const {imageClassName, titleClassName, ...propsRest} = props;
  const logoLink = useBaseUrl(logo?.href || '/');
  // If a visible title is shown, the logo is decorative, so fall back to an
  // empty alt rather than repeating the site name.
  const fallbackAlt = navbarTitle ? '' : title;
  const alt = logo?.alt ?? fallbackAlt;
  return (
    <Link
      to={logoLink}
      {...propsRest}
      {...(logo?.target && {target: logo.target})}>
      {logo && (
        <LogoThemedImage
          logo={logo}
          alt={alt}
          imageClassName={imageClassName}
        />
      )}
      {navbarTitle != null && (
        <BrandTitle title={navbarTitle} className={titleClassName} />
      )}
    </Link>
  );
}