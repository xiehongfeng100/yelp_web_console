import axios from 'axios'
const API_URL = 'http://localhost:9090/'

export default class APIService {
  getReviews (offset = 0, limit = 12) {
    const url = API_URL + 'api/reviews/' + '?' + 'offset=' + offset + '&limit=' + limit
    return axios.get(url).then(response => response.data)
  }
}
