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

  getTopNBySimilarities (userDbId, lat, lon, offset = 0, limit = 12) {
    const url = API_URL + 'api/rank/ranks/similarities/' + '?' + 'user=' + userDbId + '&lat=' + lat + '&lon=' + lon + '&offset=' + offset + '&limit=' + limit
    return axios.get(url).then(response => response.data)
  }

  getTopNByPopularities (lat, lon, offset = 0, limit = 12) {
    const url = API_URL + 'api/rank/ranks/popularities/' + '?' + 'lat=' + lat + '&lon=' + lon + '&offset=' + offset + '&limit=' + limit
    return axios.get(url).then(response => response.data)
  }

  getTopNByDists (lat, lon, offset = 0, limit = 12) {
    const url = API_URL + 'api/rank/ranks/dists/' + '?' + 'lat=' + lat + '&lon=' + lon + '&offset=' + offset + '&limit=' + limit
    return axios.get(url).then(response => response.data)
  }

  searchAndRank (keyword, lat, lon, orderBy = 'dist', offset = 0, limit = 12) {
    const url = API_URL + 'api/rank/ranks/search_and_rank/' + '?' + 'keyword=' + keyword + '&order_by=' + orderBy + '&lat=' + lat + '&lon=' + lon + '&offset=' + offset + '&limit=' + limit
    return axios.get(url).then(response => response.data)
  }
}
