
import axios from 'axios';

const base = 'movies/';

export default {
    async getAll(payload) {
        return axios
            .get(base, payload)
            .then(response => response.data);
    },
    async getMovie(id) {
        return axios.get(base + id + "/").then(response => response.data)
    },
    async getWatchlists(id) {
        return axios.get(base + id + "/watchlist/").then(response => response.data)
    },
    async addToWatchlist(id) {
        return axios.post(base + id + "/watchlist/").then(response => response.data)
    },
    async removeFromWatchlist(id) {
        return axios.delete(base + id + "/watchlist/").then(response => response.data)
    },
};