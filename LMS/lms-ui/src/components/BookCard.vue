<template>
  <div class="book" v-if="bookDetail">
    <img :src="getImagePath(bookDetail.book_cover)" :alt="bookDetail.book_name">
    <div class="des">
      <h5>{{ truncateBookName(bookDetail.book_name) }}</h5>
      <div class="star">
        <i v-for="star in bookDetail.avg_rating" :key="star" class="fas fa-star"></i>
      </div>
      <div class="bottom">
        <h4>₹{{ bookDetail.book_price }}</h4>
        <router-link :to="{ name: 'book_view', params: { book_id: bookDetail.book_id } }">
          <button>
            <i class="fa-solid fa-arrow-right"></i>
          </button>
        </router-link>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="spinner"></div>
  </div>
</template>

<script>
import { getImagePath } from '@/utilities/utilities'

export default {
  name: "BookCard",
  props: {
    book_id: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      bookDetail: null
    }
  },
  methods: {
    getImagePath,
    truncateBookName(name) {
      return name.length > 25 ? name.slice(0, 25) + '...' : name;
    },
    async fetchData() {
      try {
        const response = await fetch(`http://localhost:5000/api/book/${this.book_id}?type=BRIEF`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        if (response.ok) {
          const data = await response.json();
          this.bookDetail = data.book;
        } else if (response.status == 404) {
          this.book = null;
        } else {
          this.$router.replace('/error');
        }
      } catch (error) {
        console.error("Error fetching book data:", error);
        // Handle error as needed
      }
    }
  },
  async created() {
    await this.fetchData();
  },
  watch: {
    book_id(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.fetchData();
      }
    }
  }
}
</script>


<style>
.book {
    width:auto;
    min-width: 250px;
    padding: 10px 12px;
    border: 1px solid #cce7d0;
    background-color: #fff;
    border-radius: 20px;
    margin: 15px 0;
    margin-right: 10px;
    transition: 0.2s ease;
    display: inline-block;

}

.book:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); 
}


.book img {
    width: 100%;
    height: 300px;
    border-radius: 20px;
}

.book .des {
    text-align: start;
    padding: 10px 0;
}

.book .des span {
    padding-left: 7px;
    color: #606063;
    font-size: 12px;
}

.book .des h5 {
    padding-left: 7px;
    color: #1a1a1a;
    font-size: 14px;
    font-weight: bold;
    text-overflow: clip;
}

.book .des .star {
    padding-left: 7px;
    font-size: 12px;
    color: rgb(243, 181, 25);
}


.book .des h4 {
    padding-left: 7px;
    padding-top: 7px;
    font-size: 15px;
    font-weight: 700;
    color: #23a2f6;
}

.bottom {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.bottom button {
    margin-left: 10px;
    background-color: #ad8018;
    border: none;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    align-self: flex-end;
    cursor: pointer;
}

.bottom button:hover {
    transform: scale(1.1);
}

.bottom button i {
    color: #fff;
}
</style>