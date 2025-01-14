// store.js

import { createStore } from 'vuex';
import auth from './auth';
import master from './master';
const store = createStore({
  modules: {
    auth,
    master
  }
});

export default store
