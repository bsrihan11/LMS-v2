<template>
  <router-view></router-view>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import "@/assets/style.css"
export default {
  name: 'RootView',
  methods: {
    ...mapActions('auth', ['loadUser'])
  },
  // created() {
  //   this.loadUser();
  // }
}
</script>
