import {GetTopicTopicFragment, GetTopicUserFragment} from '../../schema/graphql-types';
import * as faker from "faker";

const originalPosterFaker = (): GetTopicUserFragment => ({
  id: faker.finance.account(),
  alias: faker.internet.userName(),
});

export const topicFaker = (): GetTopicTopicFragment => {
  const originalPoster = originalPosterFaker();
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
      ],
      timeStart: faker.date.recent().toDateString(),
      timeEnd: faker.date.recent().toDateString(),
      messages: [
        {
          id: faker.finance.account(),
          text: faker.lorem.paragraph(),
          author: {
            id: faker.finance.account(),
            alias: faker.internet.userName(),
          },
          time: faker.date.recent().toDateString(),
        }
      ],
    }
  }
};