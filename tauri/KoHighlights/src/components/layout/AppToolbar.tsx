import { useState } from 'react';
import { useAppStore } from '@/store/app-store';
import { useScan } from '@/hooks/useScan';
import { AboutDialog } from '@/components/dialogs/AboutDialog';
import { ExportDialog } from '@/components/dialogs/ExportDialog';
import { MergeDialog } from '@/components/dialogs/MergeDialog';
import { DeleteDialog } from '@/components/dialogs/DeleteDialog';
import { ArchiveDialog } from '@/components/dialogs/ArchiveDialog';

interface AppToolbarProps {
  onToggleFilter: () => void;
}

export function AppToolbar({ onToggleFilter }: AppToolbarProps) {
  const { viewMode, dbMode, isScanning, selectedBooks, setViewMode, setDbMode, clearAll } = useAppStore();
  const scan = useScan();

  const [showAbout, setShowAbout] = useState(false);
  const [showExport, setShowExport] = useState(false);
  const [showMerge, setShowMerge] = useState(false);
  const [showDelete, setShowDelete] = useState(false);
  const [showArchive, setShowArchive] = useState(false);

  const handleClear = () => {
    if (confirm('Clear all data? This cannot be undone.')) {
      clearAll();
    }
  };

  return (
    <>
      <div className="bg-white border-b border-gray-200 px-4 py-2 flex gap-2 items-center">
        <button
          onClick={() => scan.mutate()}
          disabled={isScanning}
          className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {isScanning ? 'Scanning...' : 'Scan'}
        </button>

        <div className="flex gap-1 border-l border-r px-2">
          <button
            onClick={() => setShowExport(true)}
            disabled={selectedBooks.length === 0}
            className="px-2 py-1 text-sm hover:bg-gray-100 rounded disabled:opacity-50"
          >
            Export
          </button>
          <button
            onClick={() => setShowMerge(true)}
            disabled={selectedBooks.length !== 2}
            className="px-2 py-1 text-sm hover:bg-gray-100 rounded disabled:opacity-50"
          >
            Merge
          </button>
          <button
            onClick={() => setShowDelete(true)}
            disabled={selectedBooks.length === 0}
            className="px-2 py-1 text-sm hover:bg-gray-100 rounded disabled:opacity-50"
          >
            Delete
          </button>
        </div>

        <button
          onClick={() => setShowArchive(true)}
          disabled={selectedBooks.length === 0}
          className="px-2 py-1 text-sm hover:bg-gray-100 rounded disabled:opacity-50"
        >
          Archive
        </button>
        <button
          onClick={handleClear}
          className="px-2 py-1 text-sm hover:bg-gray-100 rounded"
        >
          Clear
        </button>

        <button
          onClick={onToggleFilter}
          className="px-2 py-1 text-sm hover:bg-gray-100 rounded"
        >
          Filter
        </button>

        <div className="flex gap-2 ml-auto">
          <div className="flex gap-1 border px-2 py-1 rounded">
            <button
              type="button"
              onClick={() => setViewMode('books')}
              className={`px-2 text-sm ${viewMode === 'books' ? 'bg-blue-100' : 'hover:bg-gray-100'} rounded`}
            >
              Books
            </button>
            <button
              type="button"
              onClick={() => setViewMode('highlights')}
              className={`px-2 text-sm ${viewMode === 'highlights' ? 'bg-blue-100' : 'hover:bg-gray-100'} rounded`}
            >
              Highlights
            </button>
          </div>

          <div className="flex gap-1 border px-2 py-1 rounded">
            <button
              type="button"
              onClick={() => setDbMode(false)}
              className={`px-2 text-sm ${!dbMode ? 'bg-blue-100' : 'hover:bg-gray-100'} rounded`}
            >
              Loaded
            </button>
            <button
              type="button"
              onClick={() => setDbMode(true)}
              className={`px-2 text-sm ${dbMode ? 'bg-blue-100' : 'hover:bg-gray-100'} rounded`}
            >
              Archived
            </button>
          </div>

          <button
            onClick={() => setShowAbout(true)}
            className="px-2 py-1 text-sm hover:bg-gray-100 rounded"
          >
            About
          </button>
        </div>
      </div>

      {showAbout && <AboutDialog onClose={() => setShowAbout(false)} />}
      {showExport && <ExportDialog books={selectedBooks} onClose={() => setShowExport(false)} />}
      {showMerge && <MergeDialog selectedBooks={selectedBooks} onClose={() => setShowMerge(false)} />}
      {showDelete && <DeleteDialog selectedBooks={selectedBooks} onClose={() => setShowDelete(false)} />}
      {showArchive && <ArchiveDialog selectedBooks={selectedBooks} onClose={() => setShowArchive(false)} />}
    </>
  );
}
