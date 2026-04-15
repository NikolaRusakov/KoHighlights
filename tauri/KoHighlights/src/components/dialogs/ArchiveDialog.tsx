import { useMutation } from '@tanstack/react-query';
import { archiveBooks } from '@/api';
import { useAppStore } from '@/store/app-store';
import { Book } from '@/types';

interface ArchiveDialogProps {
  selectedBooks: Book[];
  onClose: () => void;
}

export function ArchiveDialog({ selectedBooks, onClose }: ArchiveDialogProps) {
  const { removeBooks } = useAppStore();

  const mutation = useMutation({
    mutationFn: () => archiveBooks(selectedBooks),
    onSuccess: () => {
      removeBooks(selectedBooks.map((b) => b.md5));
      alert(`Archived ${selectedBooks.length} book(s)`);
      onClose();
    },
    onError: (error) => {
      alert(`Archive failed: ${error.message}`);
    },
  });

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-md">
        <h2 className="text-xl font-bold mb-4">Archive Books</h2>

        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-3">Archive {selectedBooks.length} book(s)?</p>
          <div className="max-h-40 overflow-y-auto space-y-1">
            {selectedBooks.map((book) => (
              <div key={book.md5} className="text-xs bg-gray-50 p-1 rounded">
                {book.title}
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-500 mt-3">Archived books can be viewed from the "Archived" tab.</p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => mutation.mutate()}
            disabled={mutation.isPending}
            className="flex-1 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {mutation.isPending ? 'Archiving...' : 'Archive'}
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
