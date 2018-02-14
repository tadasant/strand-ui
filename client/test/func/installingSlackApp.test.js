import MemoryRouter from 'react-router-dom/MemoryRouter';
import App from 'src/App.react';
import Install from 'src/install/Install.react';
import React from 'react';
import {mount} from 'enzyme';
import PropTypes from 'prop-types';

describe('installing slack app', () => {
  it('renders the page when a user clicks the navigation button', () => {
    // TODO go to /, click nav button, snapshot
    const wrapper = mount(
      <MemoryRouter initialEntries={['/']}>
        <App/>
      </MemoryRouter>,
      {
        context: {uiHost: 'localhost'},
        childContextTypes: {uiHost: PropTypes.string}
      }
    );
    expect(wrapper.find(Install)).toHaveLength(1);
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
