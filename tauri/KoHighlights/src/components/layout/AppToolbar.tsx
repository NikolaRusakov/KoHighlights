import { useAppStore } from '@/store/app-store';

interface AppToolbarProps {
  onToggleFilter: () => void;
}

export function AppToolbar({ onToggleFilter }: AppToolbarProps) {
  const { viewMode, dbMode, isScanning, setViewMode, setDbMode } = useAppStore();

  return (
    <div className="bg-white border-b border-gray-200 px-4 py-2 flex gap-2 items-center">
      <button
        disabled={isScanning}
        className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {isScanning ? 'Scanning...' : 'Scan'}
      </button>

      <div className="flex gap-1 border-l border-r px-2">
        <button className="px-2 py-1 text-sm hover:bg-gray-100 rounded">Export</button>
        <button className="px-2 py-1 text-sm hover:bg-gray-100 rounded">Merge</button>
        <button className="px-2 py-1 text-sm hover:bg-gray-100 rounded">Delete</button>
      </div>

      <button className="px-2 py-1 text-sm hover:bg-gray-100 rounded">Archive</button>
      <button className="px-2 py-1 text-sm hover:bg-gray-100 rounded">Clear</button>

      <button
        onClick={onToggleFilter}
        className="px-2 py-1 text-sm hover:bg-gray-100 rounded"
      >
        Filter
      </button>

      <div className="flex gap-2 ml-auto">
        <div className="flex gap-1 border px-2 py-1 rounded">
          <button
            onClick={() => setViewMode('books')}
            className={`px-2 text-sm ${viewMode === 'books' ? 'bg-blue-100' : 'hover:bg-gray-100'} rounded`}
          >
            Books
          </button>
          <button
            onClick={() => setViewMode('highlights')}
            className={`px-2 text-sm ${viewMode === 'highlights' ? 'bg-blue-100' : 'hover:bg-gray-100'} rounded`}
          >
            Highlights
          </button>
        </div>

        <div className="flex gap-1 border px-2 py-1 rounded">
          <button
            onClick={() => setDbMode(false)}
            className={`px-2 text-sm ${!dbMode ? 'bg-blue-100' : 'hover:bg-gray-100'} rounded`}
          >
            Loaded
          </button>
          <button
            onClick={() => setDbMode(true)}
            className={`px-2 text-sm ${dbMode ? 'bg-blue-100' : 'hover:bg-gray-100'} rounded`}
          >
            Archived
          </button>
        </div>

        <button className="px-2 py-1 text-sm hover:bg-gray-100 rounded">About</button>
      </div>
    </div>
  );
}
