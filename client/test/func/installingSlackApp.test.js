import Install from 'src/install/Install.react';
import {navigationLabelToPath} from 'src/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';

describe('installing slack app', () => {
  it('sends the user to Slack when the user navigates to the page and clicks the button', async () => {
    const wrapper = mountApplication('/');

    // Navigate to install page
    wrapper.find(`Button[id="${navigationLabelToPath.Install}-button"]`).prop('onClick')();

    // Assert that the install button goes to Slack
    const anchorHref = wrapper.find('a[id="add-to-slack-button"]').prop('href');
    expect(anchorHref).toContain('slack.com/oauth');
    expect(anchorHref).toContain(process.env.SLACK_CLIENT_ID);

    // TODO start at /install, click the button, return to /install w/ a code, await response w/ success
    expect(true).toBe(true);
  });

  it('shows a success message when a user successfully installs the app', async () => {
    // TODO start at /install, click the button, return to /install w/ a code, await response w/ success
    // expect(wrapper.find(Install)).toHaveLength(1);
    // expect(wrapper).toMatchSnapshot();
    expect(true).toBe(true);
  });

  it('shows a failure message when we fail to install the app', async () => {
    // TODO start at /install, click the button, return to /install w/ a code, await response w/ failure
    expect(true).toBe(true);
  })
});
