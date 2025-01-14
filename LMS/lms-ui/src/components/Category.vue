<template>
  <div class="category p1">
    <h2>{{ name }}</h2>
    <section class="feature">
      <div v-for="(item, index) in list" :key="index">
        <div class="fe-box">
          <img :src="getImagePath(item.section_cover)" alt="No images">
          <router-link :to="{ name: 'section_view', params: { section_id: item.section_id }, query:{page_num:1} }">
            {{ item.section_name }}
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>

import { getImagePath } from "@/utilities/utilities"
export default {
  name: "Category",
  props: {
    name: {
      type: String,
      required: true
    },
    list: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
    }
  }
  ,
  methods: {
    getImagePath
  }
}
</script>

<style>
.category {
  display: flex;
  flex-direction: column;
  text-align: center;
}

.category h2 {
  padding-top: 20px;
}

.feature {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.feature .fe-box {
  width: 180px;
  text-align: center;
  padding: 25px 15px;
  box-shadow: 20px 20px 34px rgba(0, 0, 0, 0.03);
  border: 1px solid #cce7d0;
  border-radius: 4px;
  margin: 15px 10px;
  background-color: #fff;
}

.feature .fe-box:hover {
  box-shadow: 10px 10px 54px rgba(70, 62, 221, 0.1);
}

.feature .fe-box a {
  text-decoration: none;
  font-size: 25px;
  display: inline-block;
  padding: 9px 8px 6px 8px;
  line-height: 1;
  border-radius: 4px;
  color: #23a2f6;


}

.feature .fe-box img {
  width: 100%;
  margin-bottom: 10px;
}
</style>