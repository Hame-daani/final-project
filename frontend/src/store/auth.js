import Axios from 'axios';
import AuthService from '@/services/AuthService';

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
        async login({ commit }, payload) {
            return AuthService.login(payload)
                .then(result => {
                    commit('SET_TOKEN', result.token);
                    commit('SET_USER', result.user);
                    // set auth header
                    Axios.defaults.headers.common['AUTHORIZATION'] = `token ${result.token}`;
                })
        },
        logout: ({ commit }) => {
            commit('RESET', '');
        }
    },
}