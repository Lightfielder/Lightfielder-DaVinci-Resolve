import React from 'react';

// Inline, responsive 16:9 YouTube video embed for MDX articles.
// Usage: <YouTube id="MQZb7zJXfXA" title="Lightfielder Viewport" />
// Optionally pass start={seconds} to begin at a timestamp.
export default function YouTube({ id, title = 'YouTube video', start }) {
  const params = new URLSearchParams({ rel: '0' });
  if (start) {
    params.set('start', String(start));
  }
  return (
    <div className="youtube_video">
      <iframe
        src={`https://www.youtube-nocookie.com/embed/${id}?${params.toString()}`}
        title={title}
        loading="lazy"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowFullScreen
      />
    </div>
  );
}
