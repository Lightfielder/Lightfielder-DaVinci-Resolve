import MDXComponents from '@theme-original/MDXComponents';
import DocNote from '@site/src/components/DocNote';
import DocWarn from '@site/src/components/DocWarn';
import DocHeader from '@site/src/components/DocHeader';
import DocIndex from '@site/src/components/DocIndex';
import DocTitle from '@site/src/components/DocTitle';
import YouTube from '@site/src/components/YouTube';
import YouTubePlaylist from '@site/src/components/YouTubePlaylist';

// Extend the default MDX mapping (which wires up Prism code highlighting,
// themed images, headings, admonitions, etc.) with the Lightfielder doc
// components. Spreading @theme-original is required — without it the whole
// default mapping is dropped and <pre> code blocks render unhighlighted.
export default {
  ...MDXComponents,
  DocNote,
  DocWarn,
  DocHeader,
  DocIndex,
  DocTitle,
  YouTube,
  YouTubePlaylist,
};
