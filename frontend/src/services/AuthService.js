// src/services/AuthService.js

import axios from 'axios';

const url = 'http://localhost:8000/api/auth/';

export default {
    async login(payload) {
        return axios
            .post(url + 'login/', payload)
            .then(response => response.data);
    },
    async signUp(payload) {
        return axios
            .post(url + 'register/', payload)
            .then(response => response.data);
    },
};