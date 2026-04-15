interface AboutDialogProps {
  onClose: () => void;
}

export function AboutDialog({ onClose }: AboutDialogProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-sm">
        <h2 className="text-xl font-bold mb-4">About KoHighlights</h2>
        <div className="space-y-2 text-sm mb-4">
          <p><strong>Version:</strong> 2.0.0</p>
          <p><strong>Platform:</strong> Tauri v2 + React 19</p>
          <p><strong>Database:</strong> SQLite + DuckDB</p>
          <p className="text-gray-600 mt-4">
            KoHighlights manages and synchronizes highlights from KOReader across devices.
          </p>
        </div>
        <button
          onClick={onClose}
          className="w-full px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Close
        </button>
      </div>
    </div>
  );
}
