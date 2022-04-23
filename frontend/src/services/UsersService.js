
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
    },
    async getfollowing(id, payload) {
        return axios.get(base + id + "/following/", payload).then((res) => res.data)
    },
    async getfollowers(id, payload) {
        return axios.get(base + id + "/followers/", payload).then((res) => res.data)
    },
    async isfollowing(id) {
        return axios.get(base + id + "/isfollowing/").then((res) => res.data)
    },
    async isfollows(id) {
        return axios.get(base + id + "/isfollows/").then((res) => res.data)
    },
    async follow(id) {
        return axios.post(base + id + "/follow/").then((res) => res.data)
    },
    async unfollow(id) {
        return axios.post(base + id + "/unfollow/").then((res) => res.data)
    },

};