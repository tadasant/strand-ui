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
      id: string,
      alias: string,
    } | null,
    discussion:  {
      status: string,
      participants:  Array< {
        id: string,
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

export interface GetReferenceDataQuery {
  tags:  Array< {
    name: string,
  } | null > | null,
  users:  Array< {
    id: string,
    alias: string,
  } | null > | null,
};

export interface GetTopicsTopicsFragment {
  title: string,
  description: string,
  tags:  Array< {
    name: string,
  } | null > | null,
  originalPoster:  {
    id: string,
    alias: string,
  } | null,
  discussion:  {
    status: string,
    participants:  Array< {
      id: string,
      alias: string,
    } | null > | null,
  } | null,
};

export interface GetTopicsTagsFragment {
  name: string,
};

export interface GetTopicsOriginalPosterFragment {
  id: string,
  alias: string,
};

export interface GetTopicsDiscussionFragment {
  status: string,
  participants:  Array< {
    id: string,
    alias: string,
  } | null > | null,
};

export interface GetTopicsParticipantsFragment {
  id: string,
  alias: string,
};

export interface ReferenceTagsFragment {
  name: string,
};

export interface ReferenceUsersFragment {
  id: string,
  alias: string,
};
