/* tslint:disable */
//  This file was automatically generated and should not be edited.

export interface GetStrandListQueryVariables {
  query?: string | null,
  page?: number | null,
  size?: number | null,
};

export interface GetStrandListQuery {
  strands:  Array< {
    id: string,
    title: string | null,
    tags:  Array< {
      name: string,
    } | null > | null,
    saver:  {
      id: string,
      email: string,
      firstName: string,
      lastName: string,
    } | null,
  } | null > | null,
};

export interface GetReferenceDataQuery {
  tags:  Array< {
    name: string,
  } | null > | null,
  users:  Array< {
    id: string,
    email: string,
  } | null > | null,
  me:  {
    id: string,
    email: string,
  } | null,
};

export interface GetStrandDetailQueryVariables {
  id: number,
};

export interface GetStrandDetailQuery {
  strand:  {
    id: string,
    title: string | null,
    body: string,
    tags:  Array< {
      name: string,
    } | null > | null,
    saver:  {
      id: string,
      email: string,
      firstName: string,
      lastName: string,
    } | null,
  } | null,
};

export interface GetStrandListStrandsFragment {
  id: string,
  title: string | null,
  tags:  Array< {
    name: string,
  } | null > | null,
  saver:  {
    id: string,
    email: string,
    firstName: string,
    lastName: string,
  } | null,
};

export interface GetStrandListTagsFragment {
  name: string,
};

export interface GetStrandListUserFragment {
  id: string,
  email: string,
  firstName: string,
  lastName: string,
};

export interface ReferenceTagsFragment {
  name: string,
};

export interface ReferenceUsersFragment {
  id: string,
  email: string,
};

export interface ReferenceMeFragment {
  id: string,
  email: string,
};

export interface GetStrandDetailStrandFragment {
  id: string,
  title: string | null,
  body: string,
  tags:  Array< {
    name: string,
  } | null > | null,
  saver:  {
    id: string,
    email: string,
    firstName: string,
    lastName: string,
  } | null,
};

export interface GetStrandDetailTagsFragment {
  name: string,
};

export interface GetStrandDetailUserFragment {
  id: string,
  email: string,
  firstName: string,
  lastName: string,
};
