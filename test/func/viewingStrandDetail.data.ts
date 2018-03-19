import {GetStrandDetailStrandFragment, GetStrandDetailUserFragment} from '../../schema/graphql-types';
import * as faker from 'faker';

const saverFaker = (): GetStrandDetailUserFragment => ({
  id: faker.finance.account(),
  email: faker.internet.email(),
});

export const strandFaker = (): GetStrandDetailStrandFragment => {
  const saver = saverFaker();
  return {
    id: faker.finance.account(),
    title: faker.lorem.sentence(),
    tags: [
      {
        name: faker.company.bsNoun(),
      },
      {
        name: faker.company.bsNoun(),
      }
    ],
    body: faker.lorem.paragraph(),
    saver: saver,
  }
};