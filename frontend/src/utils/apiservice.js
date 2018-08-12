import axios from 'axios'
const API_URL = 'http://localhost:9090/'

export default class APIService {
  getReviews (offset = 0, limit = 12) {
    const url = API_URL + 'api/base/reviews/' + '?' + 'offset=' + offset + '&limit=' + limit
    return axios.get(url).then(response => response.data)
  }

  getTopNByFriends (userDbId, lat, lon, offset = 0, limit = 12) {
    const url = API_URL + 'api/rank/ranks/friends/' + '?' + 'user=' + userDbId + '&lat=' + lat + '&lon=' + lon + '&offset=' + offset + '&limit=' + limit
    return axios.get(url).then(response => response.data)
  }
}
