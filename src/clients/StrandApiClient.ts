// For non-graphql interaction

import {AxiosPromise} from 'axios';
import axios from 'axios';

export interface AuthTokenResponseData {
  token?: string
  error?: string
}

class StrandApiClient {
  host: string;

  constructor(host: string) {
    this.host = host;
  }

  login(email: string, password: string): AxiosPromise<AuthTokenResponseData> {
    return axios.post(`${this.host}/auth-token`, {email, password})
  }
}

export default StrandApiClient;
