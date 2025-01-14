<template>
  <div v-if='loading' class="spinner" style="text-align:center;margin:0 auto;"></div>
  <div v-else>
    <div class="p1" style="height:fit-content;min-height:100vh;">
      <header class="master-header">
        <div class="master-logo">LMS</div>
        <nav class="master-nav">
          <ul>
            <li><router-link to='/master/manager/book'>Book</router-link></li>
            <li><router-link to='/master/manager/section'>Section</router-link></li>
            <li><router-link to='/master/manager/author'>Author</router-link></li>
          </ul>
        </nav>
        <button @click="$store.dispatch('auth/logout')">logout</button>
      </header>
      <router-view name="manager"></router-view>
    </div>
    <Footer></Footer>
  
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import Footer from "@/components/Footer.vue";
export default {
  name: 'ManagerView',
  components: { Footer },
  data() {
    return {
      loading: false
    }
  },
  methods: {
  },
  computed: {
    ...mapState('auth', ['user'])
  },
  async created() {
    await this.$store.dispatch('auth/loadUser');
    if (!this.$store.state.auth.logged) {
      this.$router.replace('/master/login')
    }
    else if (this.user.role === 'USER') {
      await this.$store.dispatch('auth/logout');
      this.$router.replace('/master/login')
    }
    else {
      this.loading = false;
    }

  }
};
</script>


<style scoped>
.master-header {
  background: #1845ad;
  color: #fff;
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: fit-content;
  margin: 0 auto;
  padding: 0px 10px;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
}

.master-logo {
  font-size: 20px;
  border-radius: 20px;
  padding: 5px;
  background-color: #fff;
  color: #1845ad;
}

.master-nav {
  display: flex;
  justify-content: space-around;
}

.master-nav ul {
  list-style: none;
  display: flex;
}

.master-nav li {
  margin-right: 10px;
}

.master-nav a {
  border: none;
  color: #fff;
  text-decoration: none;
  font-size: 20px;
}

.master-nav a:hover {
  text-decoration: underline;
}

.master-header button {
  background: #ad8018;
  color: #fff;
  border:none;
  padding: 10px;
  font-size: 20px;
  border-radius: 10px;
  cursor: pointer;
}

.master-header button:hover {
  transform: scale(0.95);

}
</style>