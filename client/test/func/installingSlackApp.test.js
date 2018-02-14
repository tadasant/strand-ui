import Install from 'src/install/Install.react';
import {navigationLabelToPath} from 'src/shell/common/MenuConstants';
import {mountApplication} from 'test/helper/applicationMock';

describe('installing slack app', () => {
  it('renders the page when a user clicks the navigation button (desktop)', () => {
    const wrapper = mountApplication('/');

    wrapper.find(`Button[id="${navigationLabelToPath.Install}-button"]`).prop('onClick')();

    expect(wrapper.find(Install)).toHaveLength(1);
    expect(wrapper).toMatchSnapshot();
  });

  it('shows a success message when a user successfully installs the app', async () => {
    // TODO start at /install, click the button, return to /install w/ a code, await response w/ success
    expect(true).toBe(true);
  });

  it('shows a failure message when we fail to install the app', async () => {
    // TODO start at /install, click the button, return to /install w/ a code, await response w/ failure
    expect(true).toBe(true);
  })
});
