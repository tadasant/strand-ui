interface NavigationPaths {
  [label: string] : string,
}

export const navigationLabelToPath: NavigationPaths = {
  Install: '/install',
  Strands: '/strands',
};

export default {navigationLabelToPath};
