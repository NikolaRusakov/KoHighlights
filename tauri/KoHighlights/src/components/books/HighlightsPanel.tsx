import { useAppStore } from '@/store/app-store';

export function HighlightsPanel() {
  const { selectedBooks, selectedHighlights } = useAppStore();

  if (selectedBooks.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        Select a book to view highlights
      </div>
    );
  }

  const book = selectedBooks[0];
  const highlights = book.highlights || [];

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="px-3 py-2 border-b bg-gray-50 font-semibold text-sm">
        Highlights ({highlights.length})
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 p-3">
        {highlights.map((h, idx) => (
          <div
            key={idx}
            className="p-2 bg-gray-100 rounded border-l-4 border-blue-500 hover:bg-gray-200 transition"
            onMouseEnter={(e) => e.currentTarget.classList.add('ring-1', 'ring-blue-300')}
            onMouseLeave={(e) => e.currentTarget.classList.remove('ring-1', 'ring-blue-300')}
          >
            <div className="text-xs text-gray-600 mb-1">
              p.{h.page} • {h.date}
            </div>
            {h.chapter && (
              <div className="text-xs font-semibold text-gray-700 mb-1">{h.chapter}</div>
            )}
            <div className="text-sm text-gray-900 mb-1">{h.text}</div>
            {h.comment && (
              <div className="text-xs italic text-gray-600 border-t pt-1 mt-1">
                {h.comment}
              </div>
            )}
            <div className="flex gap-1 mt-2 opacity-0 hover:opacity-100 text-xs">
              <button className="px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600">
                Edit
              </button>
              <button className="px-2 py-1 bg-gray-500 text-white rounded hover:bg-gray-600">
                Copy
              </button>
              <button className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {highlights.length === 0 && (
        <div className="text-center py-8 text-gray-500">No highlights in this book</div>
      )}
    </div>
  );
}
