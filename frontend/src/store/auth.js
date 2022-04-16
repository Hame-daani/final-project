import Axios from 'axios';

const getDefaultState = () => {
    return {
        token: '',
        user: {}
    };
};
export default {
    namespaced: true,
    state: getDefaultState(),
    getters: {
        isLoggedIn: state => {
            return state.token;
        },
        getUser: state => {
            return state.user;
        }
    },
    mutations: {
        SET_TOKEN: (state, token) => {
            state.token = token;
        },
        SET_USER: (state, user) => {
            state.user = user;
        },
        RESET: state => {
            Object.assign(state, getDefaultState());
        }
    },
    actions: {
        login: ({ commit }, { token, user }) => {
            console.log("login")
            commit('SET_TOKEN', token);
            commit('SET_USER', user);
            // set auth header
            Axios.defaults.headers.common['AUTHORIZATION'] = `token ${token}`;
        },
        logout: ({ commit }) => {
            commit('RESET', '');
        }
    },
}