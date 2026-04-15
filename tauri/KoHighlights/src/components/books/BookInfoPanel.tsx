import { useState } from 'react';
import { Book } from '@/types';

interface BookInfoPanelProps {
  book: Book;
}

export function BookInfoPanel({ book }: BookInfoPanelProps) {
  const [collapsed, setCollapsed] = useState(false);

  if (!book) return null;

  return (
    <div className="border-t bg-white p-3">
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="w-full text-left flex items-center gap-2 font-semibold mb-2"
      >
        <span>{collapsed ? '▶' : '▼'}</span>
        Book Info
      </button>

      {!collapsed && (
        <div className="space-y-2 text-sm">
          <div>
            <span className="font-semibold">Title:</span> {book.title}
          </div>
          <div>
            <span className="font-semibold">Author:</span> {book.authors}
          </div>
          {book.series && (
            <div>
              <span className="font-semibold">Series:</span> {book.series}
            </div>
          )}
          {book.language && (
            <div>
              <span className="font-semibold">Language:</span> {book.language}
            </div>
          )}
          {book.pages > 0 && (
            <div>
              <span className="font-semibold">Pages:</span> {book.pages}
            </div>
          )}
          {book.keywords && (
            <div>
              <span className="font-semibold">Tags:</span> {book.keywords}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
