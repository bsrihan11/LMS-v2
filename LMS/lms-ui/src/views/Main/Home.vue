<template>
  <div>
    <Scroll name="Top Sellers" :books="top_sellers"></Scroll>
    <Category name="Sections" :list="sections"></Category>
  </div>
</template>

<script>
import Scroll from '@/components/Scroll.vue'
import Category from '@/components/Category.vue'
import { mapState } from 'vuex'
export default {
  name: 'HomeView',
  components: { Scroll, Category},
  data(){
    return{
      top_sellers:{},
      sections:{}
    }
  },
  async mounted() {
    const response = await fetch('http://localhost:5000/api/main', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    });
    const data = await response.json();

    if(response.ok){
      this.top_sellers = data.top_sellers;
      this.sections = data.sections;
    }
    else{
      this.$router.replace('/error')
    }
  }
}
</script>

