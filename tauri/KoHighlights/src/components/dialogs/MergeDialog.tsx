import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { canMerge, mergeTwoBooks } from '@/api';
import { useAppStore } from '@/store/app-store';
import { Book } from '@/types';

interface MergeDialogProps {
  selectedBooks: Book[];
  onClose: () => void;
}

export function MergeDialog({ selectedBooks, onClose }: MergeDialogProps) {
  const { replaceBook } = useAppStore();
  const [doMerge, setDoMerge] = useState(true);
  const [doSyncPosition, setDoSyncPosition] = useState(true);

  const mutation = useMutation({
    mutationFn: async () => {
      if (selectedBooks.length !== 2) throw new Error('Select exactly 2 books');
      const [a, b] = selectedBooks;

      const canMergeResult = await canMerge(a, b);
      if (!canMergeResult) throw new Error('Cannot merge: titles or versions differ');

      const result = await mergeTwoBooks(a, b, doMerge, doSyncPosition);
      return result;
    },
    onSuccess: (result) => {
      replaceBook(result.book_a);
      replaceBook(result.book_b);
      alert(`Merged: ${result.added} new, ${result.duplicates} duplicates`);
      onClose();
    },
    onError: (error) => {
      alert(`Merge failed: ${error.message}`);
    },
  });

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-md">
        <h2 className="text-xl font-bold mb-4">Merge Books</h2>

        <div className="space-y-3 mb-4">
          <p className="text-sm text-gray-600">Selected books: {selectedBooks.length}</p>
          {selectedBooks.map((book) => (
            <div key={book.md5} className="text-sm bg-gray-50 p-2 rounded">
              {book.title} - {book.authors}
            </div>
          ))}
        </div>

        <div className="space-y-2 mb-6">
          <label className="flex gap-2">
            <input type="checkbox" checked={doMerge} onChange={(e) => setDoMerge(e.target.checked)} />
            <span className="text-sm">Merge highlights</span>
          </label>
          <label className="flex gap-2">
            <input type="checkbox" checked={doSyncPosition} onChange={(e) => setDoSyncPosition(e.target.checked)} />
            <span className="text-sm">Sync reading position</span>
          </label>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => mutation.mutate()}
            disabled={mutation.isPending || selectedBooks.length !== 2}
            className="flex-1 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {mutation.isPending ? 'Merging...' : 'Merge'}
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
