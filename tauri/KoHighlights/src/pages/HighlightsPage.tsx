import { useMemo } from 'react';
import { useAppStore } from '@/store/app-store';
import { AppToolbar } from '@/components/layout/AppToolbar';
import { useState } from 'react';

export function HighlightsPage() {
  const { books, filterText } = useAppStore();
  const [showFilter, setShowFilter] = useState(false);

  const allHighlights = useMemo(() => {
    return books.flatMap((b) =>
      b.highlights.map((h) => ({ ...h, bookTitle: b.title, bookAuthors: b.authors, bookMd5: b.md5 }))
    );
  }, [books]);

  const displayedHighlights = useMemo(() => {
    if (!filterText) return allHighlights;
    return allHighlights.filter((h) =>
      h.text.toLowerCase().includes(filterText.toLowerCase()) ||
      h.comment.toLowerCase().includes(filterText.toLowerCase()) ||
      h.bookTitle.toLowerCase().includes(filterText.toLowerCase())
    );
  }, [allHighlights, filterText]);

  return (
    <div className="flex flex-col h-screen w-screen bg-gray-50">
      <AppToolbar onToggleFilter={() => setShowFilter(!showFilter)} />

      <div className="flex-1 overflow-auto border rounded m-2">
        <table className="w-full text-sm">
          <thead className="sticky top-0 bg-gray-100 border-b">
            <tr>
              <th className="px-2 py-2 text-left">Highlight</th>
              <th className="px-2 py-2 text-left">Comment</th>
              <th className="px-2 py-2 text-left">Date</th>
              <th className="px-2 py-2 text-left">Book</th>
              <th className="px-2 py-2 text-left">Author</th>
              <th className="px-2 py-2 text-right">Page</th>
              <th className="px-2 py-2 text-left">Chapter</th>
            </tr>
          </thead>
          <tbody>
            {displayedHighlights.map((h, idx) => (
              <tr key={idx} className="border-b hover:bg-blue-50">
                <td className="px-2 py-1 truncate">{h.text}</td>
                <td className="px-2 py-1 truncate text-gray-600">{h.comment}</td>
                <td className="px-2 py-1 text-xs text-gray-600">{h.date}</td>
                <td className="px-2 py-1 font-semibold truncate">{h.bookTitle}</td>
                <td className="px-2 py-1 truncate">{h.bookAuthors}</td>
                <td className="px-2 py-1 text-right font-mono text-sm">{h.page}</td>
                <td className="px-2 py-1 text-xs text-gray-600">{h.chapter}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {displayedHighlights.length === 0 && (
        <div className="text-center py-8 text-gray-500">No highlights found</div>
      )}
    </div>
  );
}
