interface NavigationPaths {
  [label: string] : string,
}

export const navigationLabelToPath: NavigationPaths = {
  Install: '/install',
  Topics: '/topics',
};

export default {navigationLabelToPath};
