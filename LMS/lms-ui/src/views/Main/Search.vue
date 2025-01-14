<template>
  <section v-if="loading" class="p1" style="display:flex;flex-direction:column;align-items:center;height:fit-content;">
    <h1>Loading...</h1>
    <div class="spinner"></div>
  </section>
  <div v-else-if="displayedProducts.length>0" class="product-list p1"> 
    <h1>Search results for: {{ title }}</h1>
    <div class="products">
      <BookCard v-for="(book_id, index) in displayedProducts" :key="index" :book_id="book_id">
      </BookCard>
    </div>
  
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1" :class="{'faded': currentPage === 1}">Prev</button>
      <div v-if= "!(currentPage-1 <= 0)">
        <button @click="goTo(currentPage-1)">{{ currentPage-1 }}</button>
      </div>
      <button @click="goTo(currentPage)" class="current-page">{{ currentPage }}</button>
      <div v-if= "!(currentPage + 1 >= Math.ceil(searchResults.length / itemsPerPage) + 1)">
        <button @click="goTo(currentPage+1)">{{ currentPage+1 }}</button>
      </div>
      <button @click="nextPage" :disabled="currentPage === totalPages" :class="{'faded':currentPage === totalPages}">Next</button>
    </div>
  </div>
  
  <section v-else class="p1">
    <h1 class="not-found">{{ message }}</h1>
  </section>
</template>

<script>
import BookCard from '@/components/BookCard.vue';
import { mapActions } from 'vuex';
export default {
  name: "SearchView.vue",
  data() {
    return {
      loading: true,
      message: null,
      searchResults: null,
      itemsPerPage: 3,
      currentPage: 1
    };
  },
  components: { BookCard },
  computed: {
    totalPages() {
      if (this.searchResults && this.searchResults.length > 0) {
        return Math.ceil(this.searchResults.length / this.itemsPerPage);
      } else {
        return 0;
      }
    },
    displayedProducts() {
      this.loading = true;
      setTimeout(() =>{
        this.loading = false
      },1000)
      if (!this.searchResults) {
        return []
      }
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;

      return this.searchResults.slice(start, end);
    },
    title() {
      return this.$route.query.q;
    }
  },
  methods: {
    ...mapActions('auth', ['setQuery']),
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    goTo(page_num) {
      this.currentPage = page_num;
    },
    async fetchData(query, page_num) {
      try {
        if (!query && !page_num) {
          this.loading = false;
          this.message = "404:Invalid request.";
          return;
        }
        this.currentPage = page_num;
        const response = await fetch(`http://localhost:5000/api/search?q=${query}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });

        const data = await response.json();
        if (response.ok) {
          this.searchResults = data.books || [];
          this.loading = false;
        } else if (response.status == 404) {
          this.message = '404: No result found.';
          this.loading = false;
        }
      } catch (error) {
        console.error("Search query failed: ", error);
      }
    }
  },
  async mounted() {
    if (this.$route.query.q) {
      this.setQuery(this.$route.query.q);
    }
    await this.fetchData(this.$route.query.q, this.$route.query.page_num);
  },
  watch: {
    '$route.query.q'(newQuery, oldQuery) {
      if (newQuery !== oldQuery) {
        this.loading = true;
        this.searchResults = [];
        this.fetchData(newQuery, 1);
      }
    }
  }
};
</script>

<style>
/* Add your CSS styles here */
.product-list {
  padding: 20px 0px;
  display: flex;
  flex-direction: column;
  align-items: center;
  height:auto;

}

.products {
  text-align: center;
}

.pagination i {
  font-size: 7px;
  margin: 0px 2px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  align-items: center;
  text-align: center;
  font-size: 15px;
  color: #1845ad;
}

.pagination button {
  padding: 5px 10px;
  margin-right: 5px;
}

.pagination .current-page {
  background-color: #ad8018;
  color: #fff;
  border: 1px solid #ad8018;
}

.pagination button {
  border: 1px solid #1845ad;
  color: #fff;
  background-color: #1845ad;
  border-radius: 5px;
  font-size: 15px;
}

.faded {
  background-color: grey !important;
  border:1px solid grey;
}
</style>
