// src/services/AuthService.js

import axios from 'axios';

const base = 'auth/';

export default {
    async login(payload) {
        return axios
            .post(base + 'login/', payload)
            .then(response => response.data);
    },
    async signUp(payload) {
        return axios
            .post(base + 'register/', payload)
            .then(response => response.data);
    },
};