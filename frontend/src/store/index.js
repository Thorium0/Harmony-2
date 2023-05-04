import { createStore } from 'vuex'

export default createStore({
    state: {
        isAuthenticated: false,
        token: '',
        isLoading: false,
        isOnLoginPage: false,
    },
    mutations: {
        setIsLoading(state, status) {
            state.isLoading = status
        },
        setIsOnLoginPage(state, status) {
            state.isOnLoginPage = status
        }
    },
    actions: {
    },
    modules: {
    },

})