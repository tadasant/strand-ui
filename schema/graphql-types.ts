/* tslint:disable */
//  This file was automatically generated and should not be edited.

export interface GetTopicsQuery {
  topics:  Array< {
    title: string,
    description: string,
    tags:  Array< {
      name: string,
    } | null > | null,
    originalPoster:  {
      alias: string,
    } | null,
    discussion:  {
      status: string,
      participants:  Array< {
        alias: string,
      } | null > | null,
    } | null,
  } | null > | null,
};

export interface AttemptInstallMutationVariables {
  code: string,
  clientId: string,
  redirectUri: string,
};

export interface AttemptInstallMutation {
  attemptSlackInstallation:  {
    slackTeam:  {
      name: string,
    } | null,
  } | null,
};

export interface GetTopicsTopicsFragment {
  title: string,
  description: string,
  tags:  Array< {
    name: string,
  } | null > | null,
  originalPoster:  {
    alias: string,
  } | null,
  discussion:  {
    status: string,
    participants:  Array< {
      alias: string,
    } | null > | null,
  } | null,
};

export interface GetTopicsTagsFragment {
  name: string,
};

export interface GetTopicsOriginalPosterFragment {
  alias: string,
};

export interface GetTopicsDiscussionFragment {
  status: string,
  participants:  Array< {
    alias: string,
  } | null > | null,
};

export interface GetTopicsParticipantsFragment {
  alias: string,
};
