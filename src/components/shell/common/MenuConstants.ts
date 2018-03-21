interface NavigationPaths {
  [label: string] : string,
}

export const navigationLabelToPath: NavigationPaths = {
  Strands: '/strands',
  Install: '/install',
  Login: '/login',
};

export default {navigationLabelToPath};
