
import axios from 'axios';

const base = 'users/';

export default {
    async update(payload) {
        return axios.patch(base + payload.id + "/", payload).then((res) => res.data)
    }
};