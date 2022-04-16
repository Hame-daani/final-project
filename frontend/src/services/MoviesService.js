
import axios from 'axios';

const base = 'movies/';

export default {
    async getAll(payload) {
        return axios
            .get(base, payload)
            .then(response => response.data);
    },
};