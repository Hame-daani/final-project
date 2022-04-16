// src/services/AuthService.js

import axios from 'axios';

const url = 'http://localhost:8000/api/auth/';

export default {
    async login(credentials) {
        return axios
            .post(url + 'login/', credentials)
            .then(response => response.data);
    },
    async signUp(credentials) {
        return axios
            .post(url + 'register/', credentials)
            .then(response => response.data);
    },
};