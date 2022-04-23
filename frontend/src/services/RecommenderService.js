
import axios from 'axios';

const base = 'rc/';

export default {
    async getGlobalRecommendation() {
        return axios.get(base + "global/recommend/").then(response => response.data)
    },
    async getFriendsRecommendation() {
        return axios.get(base + "friends/recommend/").then(response => response.data)
    },
    async getSimilarMovies(id) {
        return axios.get(base + "global/similar-movies/" + id + "/").then(response => response.data)
    },
    async getTasteGroup(payload) {
        return axios.get(base + "global/similar-users/", payload).then(response => response.data)
    }

};