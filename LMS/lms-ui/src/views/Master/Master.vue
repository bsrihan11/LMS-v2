<template>
  <router-view :key="masterKey" name="master"></router-view>
</template>

<script>
import { mapActions, mapState } from 'vuex';
export default {
  name:'MasterView',
  data() {
    return {
      masterKey:0
    }
  },
  computed:{
    ...mapState('auth',['logged'])
  },
  watch:{
    logged(newVal){
      this.masterKey++;
    }
  }
}
</script>