import {navigationLabelToPath} from 'src/components/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import InstallationStatus from 'src/components/install/InstallationStatus';
import {flushPromises} from '../helper/utilities';
import TestStrandSlackClient from '../clients/TestStrandSlackClient';

describe('installing slack app', () => {
  it('sends the user to Slack when the user navigates to the page and clicks the button', () => {
    const graphQLMocks = {
      Query: () => ({
        me: () => null, // not logged in
      })
    };
    const wrapper = mountApplication('/', {graphQLMocks});

    // Navigate to install page
    wrapper.find(`Button[id="${navigationLabelToPath.Slack}-button"]`).simulate('click');

    // Assert that the install button goes to Slack
    const anchorHref = wrapper.find('a[id="add-to-slack-button"]').prop('href');
    expect(anchorHref).toContain('slack.com/oauth');
    expect(anchorHref).toContain(process.env.SLACK_CLIENT_ID);
  });

  it('shows a success message when a user successfully installs the app', async () => {
    const strandSlackClient = global.strandSlackClient as TestStrandSlackClient;
    const mockSlackCode = '12345';
    strandSlackClient.addValidCode(mockSlackCode);

    const graphQLMocks = {
      Query: () => ({
        me: () => null, // not logged in
      })
    };
    const wrapper = mountApplication(`${navigationLabelToPath.Slack}?code=${mockSlackCode}`, {graphQLMocks});
    await flushPromises(); // wait for installation call to resolve
    wrapper.update();

    const installationStatusComponent = wrapper.find(InstallationStatus);
    expect(installationStatusComponent).toHaveLength(1);
    expect(installationStatusComponent).toMatchSnapshot();
  });

  it('shows a failure message when we fail to install the app', async () => {
    const graphQLMocks = {
      Query: () => ({
        me: () => null, // not logged in
      })
    };
    const wrapper = mountApplication(`${navigationLabelToPath.Slack}?code=12345`, {graphQLMocks});
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    const installationStatusComponent = wrapper.find(InstallationStatus);
    expect(installationStatusComponent).toHaveLength(1);
    expect(installationStatusComponent).toMatchSnapshot();
  })
});
