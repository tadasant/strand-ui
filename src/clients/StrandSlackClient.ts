import axios, {AxiosPromise} from 'axios';

export interface InstallationResponseData {
  error?: string
}

class StrandSlackClient {
  host: string;

  constructor(host: string) {
    this.host = host;
  }

  installApplication(code: string): AxiosPromise<InstallationResponseData> {
    return axios.post(`${this.host}/configure/install`, {code})
  }
}

export default StrandSlackClient;
