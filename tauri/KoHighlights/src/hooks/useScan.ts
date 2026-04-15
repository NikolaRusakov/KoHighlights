import { useMutation } from '@tanstack/react-query';
import { useAppStore } from '@/store/app-store';
import { scanDirectory, getAppDataDir } from '@/api';
import { open } from '@tauri-apps/plugin-dialog';

export function useScan() {
  const { setBooks, setScanning } = useAppStore();

  const mutation = useMutation({
    mutationFn: async (path?: string) => {
      const scanPath = path || (await open({ directory: true }));
      if (!scanPath) throw new Error('No directory selected');
      return scanDirectory(scanPath as string);
    },
    onMutate: () => setScanning(true),
    onSuccess: (books) => {
      setBooks(books);
      setScanning(false);
    },
    onError: () => setScanning(false),
  });

  return mutation;
}
