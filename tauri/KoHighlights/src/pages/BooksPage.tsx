import { useState } from 'react';
import { useAppStore } from '@/store/app-store';
import { AppToolbar } from '@/components/layout/AppToolbar';
import { FilterBar } from '@/components/layout/FilterBar';
import { BooksTable } from '@/components/books/BooksTable';
import { BookInfoPanel } from '@/components/books/BookInfoPanel';
import { HighlightsPanel } from '@/components/books/HighlightsPanel';

export function BooksPage() {
  const { viewMode, selectedBooks, selectedHighlights } = useAppStore();
  const [showFilter, setShowFilter] = useState(false);

  return (
    <div className="flex flex-col h-screen w-screen bg-gray-50">
      <AppToolbar onToggleFilter={() => setShowFilter(!showFilter)} />

      {showFilter && <FilterBar />}

      <div className="flex-1 overflow-hidden flex flex-col">
        {viewMode === 'books' ? (
          <div className="flex-1 flex gap-2 p-2 overflow-hidden">
            {/* Books panel (70%) */}
            <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
              <BooksTable />
              {selectedBooks.length > 0 && <BookInfoPanel book={selectedBooks[0]} />}
            </div>

            {/* Highlights panel (30%) */}
            <div className="w-1/3 min-w-0 overflow-hidden border-l">
              <HighlightsPanel />
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-hidden">
            {/* HighlightsView would go here */}
            <div>Highlights View - WIP</div>
          </div>
        )}
      </div>
    </div>
  );
}
