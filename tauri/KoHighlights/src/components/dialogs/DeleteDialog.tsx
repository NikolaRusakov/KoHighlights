import { useMutation } from '@tanstack/react-query';
import { deleteBooksAndFiles, deleteBooksInfo } from '@/api';
import { useAppStore } from '@/store/app-store';
import { Book } from '@/types';

interface DeleteDialogProps {
  selectedBooks: Book[];
  onClose: () => void;
}

export function DeleteDialog({ selectedBooks, onClose }: DeleteDialogProps) {
  const { removeBooks } = useAppStore();

  const mutation = useMutation({
    mutationFn: async (deleteFiles: boolean) => {
      if (deleteFiles) {
        await deleteBooksAndFiles(selectedBooks);
      } else {
        await deleteBooksInfo(selectedBooks);
      }
    },
    onSuccess: () => {
      removeBooks(selectedBooks.map((b) => b.md5));
      alert('Books deleted');
      onClose();
    },
    onError: (error) => {
      alert(`Delete failed: ${error.message}`);
    },
  });

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-md">
        <h2 className="text-xl font-bold mb-4 text-red-600">Delete Books</h2>

        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-3">Delete {selectedBooks.length} book(s):</p>
          <div className="max-h-40 overflow-y-auto space-y-1">
            {selectedBooks.map((book) => (
              <div key={book.md5} className="text-xs bg-gray-50 p-1 rounded">
                {book.title}
              </div>
            ))}
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => mutation.mutate(false)}
            disabled={mutation.isPending}
            className="flex-1 px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 disabled:opacity-50 text-sm"
          >
            Delete Metadata
          </button>
          <button
            onClick={() => mutation.mutate(true)}
            disabled={mutation.isPending}
            className="flex-1 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50 text-sm"
          >
            Delete All
          </button>
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 text-sm"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
