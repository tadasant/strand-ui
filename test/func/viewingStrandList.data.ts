import {GetStrandListStrandsFragment, GetStrandListUserFragment} from '../../schema/graphql-types';
import * as faker from 'faker';

const saverFaker = (): GetStrandListUserFragment => ({
  id: faker.finance.account(),
  email: faker.internet.userName(),
  firstName: faker.name.firstName(),
  lastName: faker.name.lastName(),
});

export const strandFaker = (): GetStrandListStrandsFragment => {
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
    saver: saver,
  }
};
