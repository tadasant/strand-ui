/* Wait until all pending Promises are resolved. */
export const flushPromises = (): Promise<Function> => {
  return new Promise(resolve => setImmediate(resolve));
};
