import {AxiosPromise} from 'axios';
import {AuthTokenResponseData} from '../../src/clients/StrandApiClient';
import TestClient, {successAxiosResponse} from './TestClient';

export interface StrandUser {
  email: string
  password: string
}

interface UsersByEmail {
  [email: string]: StrandUser
}

class TestStrandApiClient extends TestClient {
  usersByEmail: UsersByEmail;

  constructor() {
    super();
    this.usersByEmail = {};
  }

  // State management

  addUser(user: StrandUser) {
    this.usersByEmail[user.email] = user
  }

  clearState() {
    this.usersByEmail = {};
  }

  // Stubs

  login(email: string, password: string): AxiosPromise<AuthTokenResponseData> {
    if (email in this.usersByEmail && password === this.usersByEmail[email].password) {
      const response = {...successAxiosResponse};
      response.data = {token: 'successfullyRetrievedToken'};
      return Promise.resolve({...successAxiosResponse})
    }
    // TODO is this the right ERROR format
    return Promise.reject({'error': 'ERROR OCCURRED'})
  }
}

export default TestStrandApiClient;
