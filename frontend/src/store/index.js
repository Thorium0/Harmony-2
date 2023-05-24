import { createStore } from 'vuex'

export default createStore({
    state: {
        isAuthenticated: false,
        token: '',
        isLoading: false,
        selectedChannelId: null,
    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('token')) {
                state.token = localStorage.getItem('token')
                state.isAuthenticated = true
            } else {
                state.token = ''
                state.isAuthenticated = false
            }
        },
        setIsLoading(state, status) {
            state.isLoading = status
        },
        setToken(state, token) {
            state.token = token
            state.isAuthenticated = true
        },
        removeToken(state) {
            state.token = ''
            state.isAuthenticated = false
        },
        setSelectedChannelId(state, id) {
            state.selectedChannelId = id
        },
        removeSelectedChannelId(state) {
            state.selectedChannelId = null
        }
    },
    actions: {
    },
    modules: {
    },

})