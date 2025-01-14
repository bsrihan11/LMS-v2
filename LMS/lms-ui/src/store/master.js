import router from "@/router";
import { getCookie } from "@/utilities/utilities";


const master = {
    namespaced: true,
    state: {
        admin: null
    },
    mutations: {
        set_admin(state, admin) {
            state.admin = admin;
        },
        clear_admin(state) {
            state.admin = null;
        }
    },
    actions: {

        async loadAdmin({ commit, dispatch }) {
            try {
                const csrf_access_token = await dispatch('auth/getToken',{},{root:true});
                if (csrf_access_token) {
                    const response = await fetch('http://localhost:5000/api/admin', {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRF-TOKEN': csrf_access_token
                        },
                        credentials:'include'
                    })
                    const data = await response.json()
                    if (response.ok) {
                        
                        commit('set_admin', data.admin)
                    }
                    else if (response.status === 401 || response.status === 403) {
                        await dispatch('auth/logout',{},{root:true});
                        router.replace('/master/login')
                            
                    } else {
                        router.replace('/error')
                    }
                }
            }catch (error){
                console.error('Loading admin failed: ',error)
            }

        }
    },
    getters:{
        admin:() => state.admin
    }
}

export default master;