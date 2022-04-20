
import axios from 'axios';

const base = 'comments/';

export default {
    async update(id, payload) {
        return axios.patch(base + id + "/", payload).then((res) => res.data)
    },
    async delete(id) {
        return axios.delete(base + id + "/").then((res) => res.data)
    },
    async addComment(id, payload) {
        return axios.post(base + id + "/comments/", payload).then((res) => res.data)
    },
    async getComments(id, payload) {
        return axios.get(base + id + "/comments/", payload).then((res) => res.data)
    }
};