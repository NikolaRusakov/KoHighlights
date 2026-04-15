import { useState, useEffect } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import * as api from '@/api';
import { Note } from '@/types';

export function NotesPage() {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editingTitle, setEditingTitle] = useState('');
  const [editingContent, setEditingContent] = useState('');

  const { data: notes = [] } = useQuery({
    queryKey: ['notes'],
    queryFn: () => api.listNotes(),
  });

  const createMutation = useMutation({
    mutationFn: (data: { title: string; content: string }) =>
      api.createNote(data.title, data.content),
  });

  const updateMutation = useMutation({
    mutationFn: (data: { id: number; title: string; content: string }) =>
      api.updateNote(data.id, data.title, data.content),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => api.deleteNote(id),
  });

  const handleCreate = () => {
    if (editingTitle.trim() || editingContent.trim()) {
      createMutation.mutate(
        { title: editingTitle, content: editingContent },
        {
          onSuccess: () => {
            setEditingTitle('');
            setEditingContent('');
          },
        }
      );
    }
  };

  const handleSave = () => {
    if (editingId) {
      updateMutation.mutate(
        { id: editingId, title: editingTitle, content: editingContent },
        {
          onSuccess: () => setEditingId(null),
        }
      );
    }
  };

  const handleEdit = (note: Note) => {
    setEditingId(note.id);
    setEditingTitle(note.title);
    setEditingContent(note.content);
  };

  const handleDelete = (id: number) => {
    if (confirm('Delete this note?')) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="flex h-screen w-screen gap-2 bg-gray-50 p-2">
      {/* Notes list */}
      <div className="w-1/3 flex flex-col border rounded bg-white overflow-hidden">
        <div className="px-3 py-2 border-b font-semibold">Notes ({notes.length})</div>
        <div className="flex-1 overflow-y-auto">
          {notes.map((note) => (
            <div
              key={note.id}
              onClick={() => handleEdit(note)}
              className={`p-3 border-b cursor-pointer hover:bg-blue-50 ${
                editingId === note.id ? 'bg-blue-100' : ''
              }`}
            >
              <div className="font-semibold text-sm">{note.title || '(Untitled)'}</div>
              <div className="text-xs text-gray-600 truncate">{note.content}</div>
              <div className="text-xs text-gray-400 mt-1">{note.updated_at}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1 flex flex-col border rounded bg-white overflow-hidden">
        <div className="px-3 py-2 border-b font-semibold">
          {editingId ? 'Edit Note' : 'New Note'}
        </div>

        <div className="flex-1 flex flex-col p-3 gap-2">
          <input
            type="text"
            placeholder="Title"
            value={editingTitle}
            onChange={(e) => setEditingTitle(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <textarea
            placeholder="Content"
            value={editingContent}
            onChange={(e) => setEditingContent(e.target.value)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />

          <div className="flex gap-2">
            {editingId ? (
              <>
                <button
                  onClick={handleSave}
                  disabled={updateMutation.isPending}
                  className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
                >
                  Save
                </button>
                <button
                  onClick={() => setEditingId(null)}
                  className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    handleDelete(editingId);
                    setEditingId(null);
                  }}
                  className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </>
            ) : (
              <button
                onClick={handleCreate}
                disabled={createMutation.isPending}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
              >
                Create
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
