import {AxiosPromise} from 'axios';
import {InstallationResponseData} from '../../src/clients/StrandSlackClient';

const successAxiosResponse = {
  data: {},
  status: 200,
  statusText: 'OK',
  headers: {},
  config: {}
};

class TestStrandSlackClient {
  validCodes: string[];

  constructor() {
    this.validCodes = []
  }

  // State management

  addValidCode(code: string) {
    this.validCodes.push(code);
  }

  clearState() {
    this.validCodes = [];
  }

  // Stubs

  installApplication(code: string): AxiosPromise<InstallationResponseData> {
    if (this.validCodes.indexOf(code) != -1) {
      return Promise.resolve({...successAxiosResponse})
    }
    return Promise.reject({'error': 'ERROR OCCURRED'})
  }
}

export default TestStrandSlackClient;
