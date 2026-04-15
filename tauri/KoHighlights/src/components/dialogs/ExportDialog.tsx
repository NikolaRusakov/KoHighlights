import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { exportBooks } from '@/api';
import { open } from '@tauri-apps/plugin-dialog';
import { Book } from '@/types';

interface ExportDialogProps {
  books: Book[];
  onClose: () => void;
}

export function ExportDialog({ books, onClose }: ExportDialogProps) {
  const [format, setFormat] = useState('md');
  const [mode, setMode] = useState('individual');
  const [showPage, setShowPage] = useState(true);
  const [showDate, setShowDate] = useState(true);
  const [showChapter, setShowChapter] = useState(true);
  const [showComment, setShowComment] = useState(true);
  const [sortByPage, setSortByPage] = useState(false);

  const mutation = useMutation({
    mutationFn: async () => {
      const outputDir = await open({ directory: true });
      if (!outputDir) throw new Error('No directory selected');
      return exportBooks(books, format, mode, outputDir as string, showPage, showDate, showChapter, showComment, sortByPage);
    },
    onSuccess: () => {
      alert('Export completed');
      onClose();
    },
    onError: (error) => {
      alert(`Export failed: ${error.message}`);
    },
  });

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-md">
        <h2 className="text-xl font-bold mb-4">Export Highlights</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Format</label>
            <select value={format} onChange={(e) => setFormat(e.target.value)} className="w-full px-3 py-2 border rounded">
              <option value="txt">Text</option>
              <option value="md">Markdown</option>
              <option value="html">HTML</option>
              <option value="csv">CSV</option>
              <option value="json">JSON</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Mode</label>
            <select value={mode} onChange={(e) => setMode(e.target.value)} className="w-full px-3 py-2 border rounded">
              <option value="individual">Individual files</option>
              <option value="one">One file</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="flex gap-2">
              <input type="checkbox" checked={showPage} onChange={(e) => setShowPage(e.target.checked)} />
              <span className="text-sm">Show page numbers</span>
            </label>
            <label className="flex gap-2">
              <input type="checkbox" checked={showDate} onChange={(e) => setShowDate(e.target.checked)} />
              <span className="text-sm">Show dates</span>
            </label>
            <label className="flex gap-2">
              <input type="checkbox" checked={showChapter} onChange={(e) => setShowChapter(e.target.checked)} />
              <span className="text-sm">Show chapters</span>
            </label>
            <label className="flex gap-2">
              <input type="checkbox" checked={showComment} onChange={(e) => setShowComment(e.target.checked)} />
              <span className="text-sm">Show comments</span>
            </label>
            <label className="flex gap-2">
              <input type="checkbox" checked={sortByPage} onChange={(e) => setSortByPage(e.target.checked)} />
              <span className="text-sm">Sort by page</span>
            </label>
          </div>
        </div>

        <div className="flex gap-2 mt-6">
          <button
            onClick={() => mutation.mutate()}
            disabled={mutation.isPending}
            className="flex-1 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {mutation.isPending ? 'Exporting...' : 'Export'}
          </button>
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
