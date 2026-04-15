import { create } from 'zustand';
import { Book, Highlight, AppSettings } from '@/types';

export interface AppStore {
  // Data
  books: Book[];
  selectedBooks: Book[];
  displayedBooks: Book[];
  allHighlights: Highlight[];
  displayedHighlights: Highlight[];
  selectedHighlights: Highlight[];

  // UI state
  viewMode: 'books' | 'highlights';
  dbMode: boolean;
  isScanning: boolean;
  filterText: string;
  filterType: 'all' | 'highlights' | 'comments' | 'titles';
  settings: AppSettings | null;

  // Actions
  setBooks: (books: Book[]) => void;
  addBook: (book: Book) => void;
  selectBooks: (books: Book[]) => void;
  setDisplayedBooks: (books: Book[]) => void;
  setHighlights: (highlights: Highlight[]) => void;
  setDisplayedHighlights: (highlights: Highlight[]) => void;
  selectHighlights: (highlights: Highlight[]) => void;
  setViewMode: (mode: 'books' | 'highlights') => void;
  setDbMode: (archived: boolean) => void;
  setIsScanning: (scanning: boolean) => void;
  setFilter: (text: string, type: 'all' | 'highlights' | 'comments' | 'titles') => void;
  setSettings: (settings: AppSettings | null) => void;
  clearAll: () => void;
  replaceBook: (updated: Book) => void;
}

const defaultSettings: AppSettings = {
  last_dir: '',
  db_path: '',
  view_mode: 'books',
  sort_col: 'modified',
  sort_asc: false,
  window_width: 1200,
  window_height: 750,
  db_mode: false,
  show_exit_confirm: true,
  highlight_by_page: true,
  skip_version: '0.0.0.0',
  opened_times: 0,
  toolbar_size: 48,
};

export const useAppStore = create<AppStore>((set) => ({
  // Initial state
  books: [],
  selectedBooks: [],
  displayedBooks: [],
  allHighlights: [],
  displayedHighlights: [],
  selectedHighlights: [],
  viewMode: 'books',
  dbMode: false,
  isScanning: false,
  filterText: '',
  filterType: 'all',
  settings: defaultSettings,

  // Actions
  setBooks: (books) =>
    set({ books, selectedBooks: [] }),

  addBook: (book) =>
    set((state) => ({
      books: [...state.books, book],
    })),

  selectBooks: (books) =>
    set({ selectedBooks: books }),

  setDisplayedBooks: (books) =>
    set({ displayedBooks: books }),

  setHighlights: (highlights) =>
    set({ allHighlights: highlights }),

  setDisplayedHighlights: (highlights) =>
    set({ displayedHighlights: highlights }),

  selectHighlights: (highlights) =>
    set({ selectedHighlights: highlights }),

  setViewMode: (mode) =>
    set({ viewMode: mode }),

  setDbMode: (archived) =>
    set({ dbMode: archived }),

  setIsScanning: (scanning) =>
    set({ isScanning: scanning }),

  setFilter: (text, type) =>
    set({ filterText: text, filterType: type }),

  setSettings: (settings) =>
    set({ settings: settings || defaultSettings }),

  clearAll: () =>
    set({
      books: [],
      selectedBooks: [],
      displayedBooks: [],
      allHighlights: [],
      displayedHighlights: [],
      selectedHighlights: [],
      filterText: '',
    }),

  replaceBook: (updated) =>
    set((state) => ({
      books: state.books.map((b) => (b.md5 === updated.md5 ? updated : b)),
      selectedBooks: state.selectedBooks.map((b) => (b.md5 === updated.md5 ? updated : b)),
      displayedBooks: state.displayedBooks.map((b) => (b.md5 === updated.md5 ? updated : b)),
    })),
}));
