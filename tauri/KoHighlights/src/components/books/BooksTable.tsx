import { useMemo } from 'react';
import { useAppStore } from '@/store/app-store';
import { Book } from '@/types';

export function BooksTable() {
  const { books, selectedBooks, setDisplayedBooks, selectBooks } = useAppStore();

  const displayedBooks = useMemo(() => books, [books]);

  const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked) {
      selectBooks(displayedBooks);
    } else {
      selectBooks([]);
    }
  };

  const handleSelectBook = (book: Book, e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked) {
      selectBooks([...selectedBooks, book]);
    } else {
      selectBooks(selectedBooks.filter((b) => b.md5 !== book.md5));
    }
  };

  return (
    <div className="flex-1 overflow-auto border rounded">
      <table className="w-full text-sm">
        <thead className="sticky top-0 bg-gray-100 border-b">
          <tr>
            <th className="px-2 py-2 text-left">
              <input
                type="checkbox"
                checked={selectedBooks.length === displayedBooks.length && displayedBooks.length > 0}
                onChange={handleSelectAll}
              />
            </th>
            <th className="px-2 py-2 text-left cursor-pointer hover:bg-gray-200">Title</th>
            <th className="px-2 py-2 text-left cursor-pointer hover:bg-gray-200">Author</th>
            <th className="px-2 py-2 text-left cursor-pointer hover:bg-gray-200">Type</th>
            <th className="px-2 py-2 text-right cursor-pointer hover:bg-gray-200">%</th>
            <th className="px-2 py-2 text-left cursor-pointer hover:bg-gray-200">Rating</th>
            <th className="px-2 py-2 text-right cursor-pointer hover:bg-gray-200">Highlights</th>
            <th className="px-2 py-2 text-left cursor-pointer hover:bg-gray-200">Modified</th>
          </tr>
        </thead>
        <tbody>
          {displayedBooks.map((book) => (
            <tr
              key={book.md5}
              className="border-b hover:bg-blue-50 cursor-pointer"
              onDoubleClick={() => selectBooks([book])}
            >
              <td className="px-2 py-1">
                <input
                  type="checkbox"
                  checked={selectedBooks.some((b) => b.md5 === book.md5)}
                  onChange={(e) => handleSelectBook(book, e)}
                  onClick={(e) => e.stopPropagation()}
                />
              </td>
              <td className="px-2 py-1 font-semibold">{book.title}</td>
              <td className="px-2 py-1">{book.authors}</td>
              <td className="px-2 py-1 text-xs text-gray-600">{book.status}</td>
              <td className="px-2 py-1 text-right text-sm font-mono">
                {Math.round(book.percent_finished * 100)}%
              </td>
              <td className="px-2 py-1">{book.rating}</td>
              <td className="px-2 py-1 text-right font-mono text-blue-600">
                {book.highlights.length}
              </td>
              <td className="px-2 py-1 text-xs text-gray-600">{book.modified_date}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {displayedBooks.length === 0 && (
        <div className="text-center py-8 text-gray-500">No books loaded. Click Scan to find highlights.</div>
      )}
    </div>
  );
}
