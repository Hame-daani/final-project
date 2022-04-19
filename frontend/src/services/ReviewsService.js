
import axios from 'axios';

const base = 'reviews/';

export default {
    async getReview(id) {
        return axios.get(base + id + "/").then(response => response.data)
    },
    async getRecent() {
        return axios.get(base + "recent/").then(response => response.data)
    },
    async getFriendsRecent() {
        return axios.get(base + "friends/").then(response => response.data)
    },
    async getReviews(payload) {
        return axios.get(base, payload).then(response => response.data)
    },
    async create(payload) {
        return axios.post(base, payload).then(response => response.data)
    }
};