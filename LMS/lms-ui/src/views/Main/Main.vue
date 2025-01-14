<template>
  <div :key="mainKey">
    <Header></Header>
    <router-view name="main"></router-view>
    <Footer></Footer>
  </div>
    
</template>

<script>
import Header from "@/components/Header.vue"
import Footer from '@/components/Footer.vue'
import { mapActions, mapState } from 'vuex';
export default {
  name: "MainView",
  components:{ Header ,Footer},
  data(){
    return {
      mainKey:0
    }
  },
  computed:{
    ...mapState('auth',['logged'])
  },
  async created(){
    await this.$store.dispatch('auth/loadUser');
  },
  watch:{
    logged(newVal){
        this.mainKey++;
    }
  }
}
</script>

<style>


</style>