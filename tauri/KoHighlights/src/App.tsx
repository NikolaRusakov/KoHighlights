import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClientProvider, QueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import { useAppStore } from '@/store/app-store';
import { loadSettings } from '@/api';

// Placeholder pages (to be implemented)
const BooksPage = () => <div>Books Page - WIP</div>;
const HighlightsPage = () => <div>Highlights Page - WIP</div>;
const NotesPage = () => <div>Notes Page - WIP</div>;

const queryClient = new QueryClient();

function App() {
  const { setSettings } = useAppStore();

  useEffect(() => {
    // Load settings on startup
    loadSettings()
      .then(setSettings)
      .catch((err) => console.error('Failed to load settings:', err));
  }, [setSettings]);

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<BooksPage />} />
          <Route path="/highlights" element={<HighlightsPage />} />
          <Route path="/notes" element={<NotesPage />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
