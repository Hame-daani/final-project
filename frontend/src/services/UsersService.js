
import axios from 'axios';

const base = 'users/';

export default {
    async update(payload) {
        return axios.patch(base + payload.id + "/", payload).then((res) => res.data)
    },
    async getWatchlist(id, payload) {
        return axios.get(base + id + "/watchlist/", payload).then((res) => res.data)
    },
    async getFavorites(id, payload) {
        return axios.get(base + id + "/favorites/", payload).then((res) => res.data)
    },
    async getUser(id) {
        return axios.get(base + id + "/").then((res) => res.data)
    }
};