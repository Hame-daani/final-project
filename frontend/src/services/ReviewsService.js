
import axios from 'axios';

const base = 'reviews/';

export default {
    async getReview(id) {
        return axios.get(base + id + "/").then(response => response.data)
    },
    async getRecent() {
        return axios.get(base + "recent/").then(response => response.data)
    }
};