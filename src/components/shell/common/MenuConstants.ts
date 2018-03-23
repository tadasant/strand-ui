interface NavigationPaths {
  [label: string] : string,
}

export const loggedInNavigationLabelToPath: NavigationPaths = {
  Strands: '/strands',
  Slack: '/install',
};

export const navigationLabelToPath: NavigationPaths = {
  ...loggedInNavigationLabelToPath,
  Login: '/login',
};

export default {navigationLabelToPath, loggedInNavigationLabelToPath};
