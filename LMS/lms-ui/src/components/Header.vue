<template>
    <section>
        <nav>
            <router-link to="/home">LMS V2</router-link>
            <div class="searchbar">
                <input type="text" placeholder="Search for e-books" v-model="searchQuery">
                <button @click="search"><i class="fa-solid fa-magnifying-glass"></i></button>
            </div>
    
            <button v-if="logged" @click="logout()">
                Logout
                <i class="fa fa-sign-out" aria-label="Logout"></i>
            </button>
            <button v-else @click="$router.push('/auth/login')">
                Login
                <i class="fa fa-sign-in" aria-label="Login"></i>
            </button>

    
        </nav>
        <div class="nav2">
          <ul>
            <li>
              <router-link to="/home">Home</router-link>
            </li>
            <li>
              <router-link to='/profile'>Profile</router-link>
            </li>
          </ul>
        </div>
    </section>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import router from '@/router';
export default {
  name: 'Header',
  data() {
    return {
    };
  },
  methods: {
    ...mapActions('auth',['logout','setQuery']),
    search() {
      this.$router.push({ path: '/search', query: { q: this.searchQuery ,page_num:1} });
    }
  },
  computed: {
    ...mapState('auth',['logged','q']),
    searchQuery: {
      get() {
        return this.q; 
      },
      set(value) {
        this.setQuery(value); 
      },
    }
  }
};
</script>

<style>
nav {
    width: 100%;
    background: #1845ad;
    color: #fff;
    display: flex;
    align-items: center;
    font-size: 18px;
    height: 70px;

}

nav a:nth-child(1) {
    width: 7%;
    margin: 20px;
    padding: 0px 5px;
    border: 1px solid #fff;
    text-decoration: none;
    color: #fff;
    text-align: center;
    border-radius: 5px;


}

nav .searchbar {
    display: flex;
    width: 80%;

}


nav .searchbar button {
    border: none;
    outline: none;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    font-size: 20px;
    padding: 0 15px;
    background-color: #ad8018;
    cursor:pointer;

}
nav input {
    width: 100%;
    height: 40px;
    border-right: none;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    border: none;
    outline: none;
    padding: 0 10px;
    font-size: 18px;
}


nav > button{
    display: flex;
    align-items: center;
    padding: 7px;
    margin: 0 10px;
    font-size: 20px;
    width: auto;
    color: #fff;
    text-decoration: none;
    background: #1e57da;
    border: 1px solid #fff;
    border-radius: 10px;
    cursor:pointer;
}



nav i {
    color: #fff;
    margin-left: 3px;
}




.nav2 {
    display: flex;
    background-color: #1e57da;
    height: 50px;
    align-items: center;
    justify-content: space-between;
    padding: 0 30px;

}

.nav2 ul {
    display: flex;
    gap: 15px;
    align-items: center;
}

.nav2 ul li {
    list-style: none;
}

.nav2 ul li a {
    text-decoration: none;
    color: #fff;
    font-size: 15px;
    padding: 5px 8px;
}

.links {
    text-decoration: none;
    color: #fff;

}


.router-link-active {
    font-weight: bold;
    font-size: 20px;
    text-decoration: underline;
}

.router-link-active + .nav2 ul li{
  background: black;
}
</style>
