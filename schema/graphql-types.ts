/* tslint:disable */
//  This file was automatically generated and should not be edited.

export interface GetTopicsQuery {
  topics:  Array< {
    id: string,
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

export interface GetTopicQueryVariables {
  id: number,
};

export interface GetTopicQuery {
  topic:  {
    id: string,
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
      timeStart: string,
      timeEnd: string | null,
      status: string,
      participants:  Array< {
        id: string,
        alias: string,
      } | null > | null,
    } | null,
  } | null,
};

export interface GetTopicsTopicsFragment {
  id: string,
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

export interface GetTopicTopicFragment {
  id: string,
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
    timeStart: string,
    timeEnd: string | null,
    status: string,
    participants:  Array< {
      id: string,
      alias: string,
    } | null > | null,
  } | null,
};

export interface GetTopicTagsFragment {
  name: string,
};

export interface GetTopicUserFragment {
  id: string,
  alias: string,
};

export interface GetTopicDiscussionFragment {
  timeStart: string,
  timeEnd: string | null,
  status: string,
  participants:  Array< {
    id: string,
    alias: string,
  } | null > | null,
};
