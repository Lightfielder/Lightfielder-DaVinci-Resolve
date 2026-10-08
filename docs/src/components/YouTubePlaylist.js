import React from 'react';

// Inline, responsive 16:9 YouTube playlist embed for MDX articles.
// Usage: <YouTubePlaylist id="PLVDcRvd92hcgumsGnIth-hDi3gvVTc71u" title="Playlist name" />
export default function YouTubePlaylist({ id, title = 'YouTube playlist' }) {
  return (
    <div className="youtube_playlist">
      <iframe
        src={`https://www.youtube-nocookie.com/embed/videoseries?list=${id}`}
        title={title}
        loading="lazy"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowFullScreen
      />
    </div>
  );
}
