import gql from 'graphql-tag';

// TODO [UI-47]: split this huge file into .graphql files

export const GET_STRAND_LIST_QUERY = gql`
    query GetStrandList {
        strands {
            ...GetStrandListStrands
        }
    }

    fragment GetStrandListStrands on StrandType {
        id
        title
        tags {
            ...GetStrandListTags
        }
        saver {
            ...GetStrandListUser
        }
    }

    fragment GetStrandListTags on TagType {
        name
    }

    fragment GetStrandListUser on UserType {
        id
        email
        firstName
        lastName
    }
`;

export const GET_REFERENCE_DATA_QUERY = gql`
    query GetReferenceData {
        tags {
            ...ReferenceTags
        }
        users {
            ...ReferenceUsers
        }
        me {
            ...ReferenceMe
        }
    }
  
    fragment ReferenceTags on TagType {
        name
    }
  
    fragment ReferenceUsers on UserType {
        id
        email
    }
  
    fragment ReferenceMe on UserType {
        id
        email
    }
`;

export const GET_STRAND_DETAIL_QUERY = gql`
    query GetStrandDetail($id: Int!) {
        strand(id: $id) {
            ...GetStrandDetailStrand
        }
    }
    
    fragment GetStrandDetailStrand on StrandType {
        id
        title
        body
        tags {
            ...GetStrandDetailTags
        }
        saver {
            ...GetStrandDetailUser
        }
    }
  
    fragment GetStrandDetailTags on TagType {
        name
    }
  
    fragment GetStrandDetailUser on UserType {
        id
        email
        firstName
        lastName
    }
`;
