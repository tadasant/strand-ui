import {navigationLabelToPath} from 'src/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';
import InstallationStatus from 'src/install/InstallationStatus.react';

function flushPromises() {
  return new Promise(resolve => setImmediate(resolve));
}

describe('installing slack app', () => {
  it('sends the user to Slack when the user navigates to the page and clicks the button', async () => {
    const wrapper = mountApplication('/');

    // Navigate to install page
    wrapper.find(`Button[id="${navigationLabelToPath.Install}-button"]`).simulate('click');

    // Assert that the install button goes to Slack
    const anchorHref = wrapper.find('a[id="add-to-slack-button"]').prop('href');
    expect(anchorHref).toContain('slack.com/oauth');
    expect(anchorHref).toContain(process.env.SLACK_CLIENT_ID);
  });

  it('shows a success message when a user successfully installs the app', async () => {
    const mockSlackCode = '12345';
    const graphqlMocks = {
      AttemptSlackInstallationMutation: (_: any, info: any) => {
        // TODO info's "any" type above should be s.t. info.input is the AttemptSlackInstallationMutationInput
        expect(info.input.code).toEqual(mockSlackCode); // ensuring the code is pulled from the URL
        return {}
      },
    };
    const wrapper = mountApplication(`${navigationLabelToPath.Install}?code=${mockSlackCode}`, {graphqlMocks});
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    const installationStatusComponent = wrapper.find(InstallationStatus);
    expect(installationStatusComponent).toHaveLength(1);
    expect(installationStatusComponent).toMatchSnapshot();
  });

  it('shows a failure message when we fail to install the app', async () => {
    const graphqlMocks = {
      AttemptSlackInstallationMutation: () => {
        throw 'This error message should be displayed on UI'
      },
    };
    const wrapper = mountApplication(`${navigationLabelToPath.Install}?code=12345`, {graphqlMocks});
    await flushPromises(); // wait for GraphQL call to complete
    wrapper.update();

    const installationStatusComponent = wrapper.find(InstallationStatus);
    expect(installationStatusComponent).toHaveLength(1);
    expect(installationStatusComponent).toMatchSnapshot();
  })
});
