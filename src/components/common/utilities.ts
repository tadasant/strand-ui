export const filterFalsey = <T extends any>(values: (T | null | undefined)[]): T[] => {
  return values.filter(x => x) as T[];
};
