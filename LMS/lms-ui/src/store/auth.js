import router from "@/router";
import { getCookie } from "@/utilities/utilities";

const auth = {
  namespaced: true,
  state: {
    logged: false,
    user: null,
    collection: null,
    top_sellers: null,
    sections: null,
    q: '',
    message: null,
    error: null
  },
  mutations: {
    set_user(state, user) {
      state.user = user;
      state.logged = true;
    },
    clear_user(state) {
      state.user = null;
      state.logged = false;
    },
    set_collection(state, collection) {
      state.collection = collection
    },
    clear_collection(state) {
      state.collection = null
    },
    setq(state, value) {
      state.q = value;
    },
    update_rating(state, payload) {
      state.collection[payload.book_id].rating = payload.rating
    },
    return_book(state, book_id) {
      delete state.collection[book_id];
    },
    new_collection(state,payload){
      state.collection[payload.book_id] = payload.collection_details
    }
  },
  actions: {
    async update_rating({ commit }, payload) {
      commit('update_rating', payload);
    },
    async return_book({ commit }, book_id) {
      commit('return_book', book_id);
    }
    ,
    async new_collection({commit},payload){
      commit('new_collection',payload)
    },
    setQuery({ commit }, query) {
      commit('setq', query);
    },
    async getToken({ state, commit }) {
      try {
        const csrf_access_token = getCookie('csrf_access_token');
        if (csrf_access_token) return csrf_access_token;

        const csrf_refresh_token = getCookie('csrf_refresh_token');
        if (csrf_refresh_token) {
          const response = await fetch('http://localhost:5000/api/refresh', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrf_refresh_token
            },
            credentials: 'include'
          });
          const data = await response.json();
          if (response.ok) return getCookie('csrf_access_token');
        }

        commit('clear_collection');
        commit('clear_user');

        return null
      } catch (error) {
        console.error("Token error: ", error);
      }
    }
    ,
    async loadUser({ commit, dispatch }) {
      try {
        const csrf_access_token = await dispatch('getToken');
        if (csrf_access_token) {
          const response = await fetch('http://localhost:5000/api/user', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrf_access_token
            },
            credentials: 'include'
          });
          const data = await response.json();
          if (response.ok) {
            commit('set_user', data.user);
            commit('set_collection', data.collection);
          } else if (response.status == 401) {
           console.log('Error in loading data')
          }
          else {
            router.replace('/error')
          }
        }
      } catch (error) {
        console.error('Loading User failed: ', error);
      }
    },
    async login({ commit, dispatch }, payload) {
      try {
        const response = await fetch('http://localhost:5000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({
            email: payload.email,
            password: payload.password,
          }),
        });
        const data = await response.json();
        if (response.ok) {
          await dispatch('loadUser');
          return true
        } else if (response.status === 401) {
          return data.errors;
        } else {
          router.replace('/error')
        }
      } catch (error) {
        console.error('Login failed:', error);
      }
    },

    async register({ commit, dispatch }, payload) {
      try {
        const response = await fetch('http://localhost:5000/api/user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
          body: JSON.stringify({
            email: payload.email,
            password: payload.password,
            first_name: payload.first_name,
            last_name: payload.last_name
          }),
        });
        const data = await response.json();

        if (response.ok) {
          return true
        }
        else if (response.status === 401) {
          return data.errors
        }
        else {
          router.replace('/error')
        }
      }
      catch (error) {
        console.error('Registration Failed: ', error)
      }
    },
    async logout({ state,commit, dispatch }) {
      try {
        const csrf_access_token = await dispatch('getToken')
        if (csrf_access_token) {

          const response = await fetch('http://localhost:5000/api/logout', {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrf_access_token
            },
            credentials: 'include',
          });
          if (response.ok) {
            commit('clear_user');
            commit('clear_collection');
          }
          else {
            commit('clear_user');
            commit('clear_collection');
          }
        }else{
          commit('clear_user');
          commit('clear_collection');
        }

      } catch (error) {
        console.error('Logout failed:', error);
      }
    },
    async updateUser({ commit, dispatch }, payload) {
      try {
        const csrf_access_token = await dispatch('getToken');
        if (csrf_access_token) {
          const response = await fetch('http://localhost:5000/api/user', {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrf_access_token
            },
            credentials: 'include',
            body: JSON.stringify({
              email: payload.email,
              first_name: payload.first_name,
              last_name: payload.last_name
            }),
          });
          const data = await response.json();
          if (response.ok) {
            commit('set_user', data.user)
            return true
          }
          else if (response.status === 401 || response.status === 403) {
            if(data.msg){
              await dispatch('logout');
              router.replace('/profile')
            }
            return data.errors
          } else {
            router.replace('/error')
          }
        }
        else {
          let to = router.options.history.state.back
          if(to){
            router.replace(to)
          }
          else{
            router.replace('/home')
          }
        }

      } catch (error) {
        console.error('Updating user failed:', error);
      }
    }
  },
  getters: {
    logged: (state) => state.logged,
    user:(state) => state.user,
  },
};

export default auth;
