
import axios from 'axios';

const base = 'users/';

export default {
    async update(payload) {
        return axios.patch(base + payload.id + "/", payload).then((res) => res.data)
    },
    async getWatchlist(id, payload) {
        return axios.get(base + id + "/watchlist/", payload).then((res) => res.data)
    }
};