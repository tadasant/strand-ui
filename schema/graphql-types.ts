/* tslint:disable */
//  This file was automatically generated and should not be edited.

export interface attemptInstallMutationVariables {
  code: string,
  clientId: string,
  redirectUri: string,
};

export interface attemptInstallMutation {
  attemptSlackInstallation:  {
    slackTeam:  {
      name: string,
    } | null,
  } | null,
};
