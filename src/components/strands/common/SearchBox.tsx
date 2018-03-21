import * as React from 'react';
import {ChangeEvent, Component, KeyboardEvent} from 'react';
import Input from 'material-ui/Input';

interface PropTypes {
  onSearchStrands: (searchQuery: string) => void
}

interface StateTypes {
  searchValue: string
}

class SearchBox extends Component<PropTypes, StateTypes> {
  constructor(props: PropTypes) {
    super(props);
    this.state = {
      searchValue: ''
    };

    this.handlePerformSearch = this.handlePerformSearch.bind(this);
    this.handleSearchValueChange = this.handleSearchValueChange.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  handleSearchValueChange(e: ChangeEvent<HTMLInputElement>) {
    const searchValue = e.target.value;
    this.setState({searchValue});
  }

  handlePerformSearch() {
    this.props.onSearchStrands(this.state.searchValue);
  }

  handleKeyPress(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === 'Enter') {
      this.handlePerformSearch()
    }
  }

  render() {
    return (
      <Input
        autoFocus
        fullWidth
        onChange={this.handleSearchValueChange}
        onKeyDown={this.handleKeyPress}
        placeholder='Search...'
      />
    );
  }
}


export default SearchBox;
