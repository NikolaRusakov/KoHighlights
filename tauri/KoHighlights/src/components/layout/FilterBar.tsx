import { useAppStore } from '@/store/app-store';

export function FilterBar() {
  const { filterText, filterType, setFilter, displayedBooks, displayedHighlights } = useAppStore();

  const count = filterType === 'all' ? displayedBooks.length : displayedHighlights.length;

  return (
    <div className="bg-white border-b border-gray-200 px-4 py-2 flex gap-2 items-center">
      <input
        type="text"
        placeholder="Search..."
        value={filterText}
        onChange={(e) => setFilter(e.target.value, filterType)}
        className="flex-1 px-3 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <select
        value={filterType}
        onChange={(e) => setFilter(filterText, e.target.value as any)}
        className="px-3 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="all">All</option>
        <option value="highlights">Highlights</option>
        <option value="comments">Comments</option>
        <option value="titles">Titles</option>
      </select>

      <span className="text-sm text-gray-600">{count} results</span>
    </div>
  );
}
