
import axios from 'axios';


export default {
    async getLikes(base, id) {
        return axios.get(base + id + "/likes/").then((res) => res.data)
    },
    async addLike(base, id) {
        return axios.post(base + id + "/likes/").then((res) => res.data)
    },
    async deleteLike(id) {
        return axios.delete("likes/" + id + "/").then((res) => res.data)
    },
};