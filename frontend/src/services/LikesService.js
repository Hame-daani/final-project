
import axios from 'axios';


export default {
    async getLikes(base, id) {
        return axios.get(base + id + "/likes/").then((res) => res.data)
    },
    async addLike(base, id) {
        return axios.post(base + id + "/likes/").then((res) => res.data)
    },
    async deleteLike(base, id) {
        return axios.delete(base + id + "/likes/").then((res) => res.data)
    },
};