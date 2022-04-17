
import axios from 'axios';

const base = 'rc/';

export default {
    async getGlobalRecommendation() {
        return axios.get(base + "global/recommend/").then(response => response.data)
    },

};