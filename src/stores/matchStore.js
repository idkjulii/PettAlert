import { create } from 'zustand';

export const useMatchesStore = create((set) => ({
  matchesByReport: {},
  setMatchesForReport: (reportId, matchesData) =>
    set((state) => ({
      matchesByReport: {
        ...state.matchesByReport,
        [reportId]: matchesData,
      },
    })),
  clearMatchesForReport: (reportId) =>
    set((state) => {
      const updated = { ...state.matchesByReport };
      delete updated[reportId];
      return { matchesByReport: updated };
    }),
  clearAllMatches: () => set({ matchesByReport: {} }),
}));

