<template>
  <section class="scroll">
    <h2>{{ name }}</h2>
    <button class="scroll-btn left-btn" @click="scrollMenu(-1)">❮</button>
    <div class="scroll-container" :ref="name">
      <BookCard v-for="(book_id, index) in books" :key="index" :book_id="book_id">
      </BookCard>
  
    </div>
    <button class="scroll-btn right-btn" @click="scrollMenu(1)">❯</button>
  </section>
</template>

<script>
import BookCard from './BookCard.vue';


export default {
  name: 'Scroll',
  components: { BookCard },
  props: {
    name:{
      type:String,
      required:true
    },
    books:{
      type:Object,
      required:true
    }
  },
  data() {
    return {
    }
  },
  methods: {
    scrollMenu(direction) {
      const scrollAmount = 200;
      this.$refs[this.name].scrollLeft += direction * scrollAmount;
    }
  }
}
</script>


<style>
.scroll {
  position: relative;
}

.scroll h2 {
  margin: 0px 80px 0px 80px;
  padding: 20px 10px 0px 10px;
  background-color: whitesmoke;
}

.scroll h2 {
  text-align: center;
}

.scroll .scroll-container {
  display: flex;
  flex-direction: row;
  padding-top: 20px;
  overflow: hidden;
  white-space: nowrap;
  transition: transform 0.3s ease-in-out;
  position: relative;
  height: fit-content;
  margin: 0px 80px 0px 80px;
  padding: 0px 10px 0px 10px;
  background-color: whitesmoke;
  background-clip: padding-box;
  height:fit-content;
}


.scroll-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 20px;
  background-color: #ddd;
  border: none;
  cursor: pointer;
  padding: 10px;
  z-index: 200;
}

.left-btn {
  left: 50px;
}

.right-btn {
  right: 50px;
}
</style>