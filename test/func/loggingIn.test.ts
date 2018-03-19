import {navigationLabelToPath} from 'src/components/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import StrandListViewContainer from 'src/components/strands/StrandListViewContainer';
import {flushPromises} from '../helper/utilities';
import TestStrandApiClient, {StrandUser} from '../clients/TestStrandApiClient';
import * as faker from 'faker';
import Login from '../../src/components/login/Login';

describe('logging in', () => {
  xit('loads the strand page when user succeeds in logging in', async () => {
    // TODO enable this test when we have data flow for user
    const wrapper = mountApplication(`${navigationLabelToPath.Login}`);
    const strandApiClient = global.strandApiClient as TestStrandApiClient;
    const mockUser: StrandUser = {
      email: faker.internet.email(),
      password: faker.internet.password(),
    };
    strandApiClient.addUser(mockUser);

    const emailInput = wrapper.find('TextField[id="email-field"]');
    emailInput.simulate('change', {target: {value: mockUser.email}});
    const passwordInput = wrapper.find('TextField[id="password-field"]');
    passwordInput.simulate('change', {target: {value: mockUser.password}});
    wrapper.find('Button[id="login-button"]').simulate('click');
    await flushPromises(); // wait for installation call to resolve
    wrapper.update();

    // TODO assert cookie is saved
    expect(wrapper.find(StrandListViewContainer)).toHaveLength(1);
  });

  it('stays on the login page when user fails to login', async () => {
    const wrapper = mountApplication(`${navigationLabelToPath.Login}`);
    const mockUser: StrandUser = {
      email: faker.internet.email(),
      password: faker.internet.password(),
    };

    const emailInput = wrapper.find('TextField[id="email-field"]');
    emailInput.simulate('change', {target: {value: mockUser.email}});
    const passwordInput = wrapper.find('TextField[id="password-field"]');
    passwordInput.simulate('change', {target: {value: mockUser.password}});
    wrapper.find('Button[id="login-button"]').simulate('click');
    await flushPromises(); // wait for installation call to resolve
    wrapper.update();

    expect(wrapper.find(Login)).toMatchSnapshot();
  })
});
