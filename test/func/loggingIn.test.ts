import {navigationLabelToPath} from 'src/components/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import StrandListViewContainer from 'src/components/strands/StrandListViewContainer';
import {flushPromises} from '../helper/utilities';
import TestStrandApiClient, {StrandUser} from '../clients/TestStrandApiClient';
import * as faker from 'faker';
import Login from '../../src/components/login/Login';
import * as Cookies from 'js-cookie';
import {MockList} from 'graphql-tools';
import {strandFaker} from './viewingStrandList.data';

describe('logging in', () => {
  beforeEach(() => {
    faker.seed(10);
  });

  it('loads the strand page when user succeeds in logging in', async () => {
    const cookiesSpy = jest.spyOn(Cookies, 'set');
    const graphQLMocks = { // Including this so that StrandListViewContainer renders smoothly at the end
      Query: () => ({
        strands: () => new MockList(2, () => strandFaker()),
      })
    };
    const wrapper = mountApplication(`${navigationLabelToPath.Login}`, {graphQLMocks});
    const strandApiClient = global.strandApiClient as TestStrandApiClient;
    const mockUser: StrandUser = {
      email: faker.internet.email(),
      password: faker.internet.password(),
    };
    strandApiClient.addUser(mockUser);

    const emailInput = wrapper.find('TextField[id="email-field"]');
    (emailInput.prop('onChange') as any)({target: {value: mockUser.email}}); // `as any` fixes types bug
    const passwordInput = wrapper.find('TextField[id="password-field"]');
    (passwordInput.prop('onChange') as any)({target: {value: mockUser.password}}); // `as any` fixes types bug
    wrapper.find('Button[id="login-button"]').simulate('click');
    await flushPromises(); // wait for installation call to resolve
    wrapper.update();

    expect(cookiesSpy).toHaveBeenCalled();
    // TODO would be good to assert that resetStore happened
    expect(wrapper.find(StrandListViewContainer)).toHaveLength(1);
  });

  it('stays on the login page when user fails to login', async () => {
    const wrapper = mountApplication(`${navigationLabelToPath.Login}`);
    const mockUser: StrandUser = {
      email: faker.internet.email(),
      password: faker.internet.password(),
    };

    const emailInput = wrapper.find('TextField[id="email-field"]');
    (emailInput.prop('onChange') as any)({target: {value: mockUser.email}}); // `as any` fixes types bug
    const passwordInput = wrapper.find('TextField[id="password-field"]');
    (passwordInput.prop('onChange') as any)({target: {value: mockUser.password}}); // `as any` fixes types bug
    wrapper.find('Button[id="login-button"]').simulate('click');
    await flushPromises(); // wait for installation call to resolve
    wrapper.update();

    expect(wrapper.find(Login)).toMatchSnapshot();
  })
});
