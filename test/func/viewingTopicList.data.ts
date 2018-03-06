import {GetTopicsTopicsFragment, GetTopicsUserFragment} from '../../schema/graphql-types';
import * as faker from 'faker';

const fakeOriginalPoster = (): GetTopicsUserFragment => ({
  id: faker.finance.account(),
  alias: faker.internet.userName(),
});

export const fakeTopic = (): GetTopicsTopicsFragment => {
  const originalPoster = fakeOriginalPoster();
  return {
    id: faker.finance.account(),
    title: faker.lorem.sentence(),
    description: faker.hacker.phrase(),
    tags: [
      {
        name: faker.company.bsNoun(),
      },
      {
        name: faker.company.bsNoun(),
      }
    ],
    originalPoster: originalPoster,
    discussion: {
      status: faker.company.bsBuzz(),
      participants: [
        originalPoster,
        {
          id: faker.finance.account(),
          alias: faker.internet.userName(),
        }
      ]
    }
  }
};
