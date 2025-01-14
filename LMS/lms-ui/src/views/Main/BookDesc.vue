<template>
  <section v-if="loading" class="p1" style="display:flex;flex-direction:column;align-items:center;height:fit-content;">
    <h1>Loading...</h1>
    <div class="spinner"></div>
  </section>
  <section v-else-if="book" class="book-container p1">
    <!-- Left side -->
    <div class="img-card">
      <img :src="getImagePath(book.book_cover)" :alt="book.book_name">
    </div>
    <!-- Right side -->
    <div class="book-info">
      <h3>{{ book.book_name }}</h3>
      <div class="book-meta">
        <h5>Price: ₹{{ book.book_price }}</h5>
        <p>
          <b>Authors: </b>
          <span v-for="(author, index) in book.authors" :key="index">
            <b>{{ author }}</b>
            <span v-if="index !== book.authors.length - 1"> | </span>
          </span>
        </p>
        <p>Read by {{ book.vol_sold }} readers</p>
        <div style="font-size: 16px;color: #666;margin: 5px 0;">
          Rating:
          <span v-if="book.avg_rating === 0">
            Null
          </span>
          <span v-else>
            <i v-for="star in book.avg_rating" :key="star" class="fas fa-star" style="color:rgb(243, 181, 25);"></i>
          </span>
        </div>
        <p>Available for <b>{{ book.days}}</b> days</p>
        <p>Section: <b>{{book.section_name}}</b></p>
        <p>Year of publication: <b>{{book.year}}</b></p>
      </div>
      <div class="description">
        <b>DESCRIPTION</b>
        <p>{{ book.book_summary }}</p>
      </div>
      <div class="action-buttons">
        <button v-if="!logged" class="disabled">Please login first</button>
        <button v-else-if="logged && collection && collection[book.book_id]" @click="$router.push('/profile')"
          class="secondary">Go
          to Collection => </button>
        <button v-else-if="!submit" class="primary" @click="addToCollection">Add to Collection</button>
        <div v-else class="spinner"></div>
        <div v-if="errors.general" style="color:red;">{{errors.general }}</div>
      </div>
    </div>
  </section>
  
  <section v-else class="p1">
    <h1 class="not-found">404: Book not found.</h1>
  </section>
</template>

<script>
import { getImagePath } from "@/utilities/utilities";
import { mapActions, mapState } from 'vuex';

export default {
  name: "BookDesc",
  data() {
    return {
      book: null,
      loading: true,
      submit: false,
      valid: true,
      errors: {
        general: null
      }
    };
  },
  methods: {
    ...mapActions('auth', ['getToken', 'loadUser']),
    getImagePath,
    async fetchData(book_id) {
      try {
        const response = await fetch(`http://localhost:5000/api/book/${book_id}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });

        if (response.ok) {
          const data = await response.json();
          this.book = data.book;
        } else if (response.status == 404) {
          this.book = null;
        } else {
          this.$router.replace("/error");
        }
      } catch (error) {
        console.error("Error fetching book:", error);
        this.$router.replace("/error");
      } finally {
        this.loading = false;
      }
    },
    async addToCollection() {
      this.submit = true;
      const csrf_access_token = await this.getToken();
      const response = await fetch(`http://localhost:5000/api/transaction?book_id=${this.book.book_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf_access_token
        },
        credentials: 'include'
      })

      const result = await response.json();
      if (response.ok) {
        let payload = { book_id: this.book.book_id, collection_details: result.new_collection }
        this.$store.dispatch('auth/new_collection', payload)

        this.submit = false;
      }
      else if (response.status === 401 || response.status === 404) {
        if (result.msg) {
          this.errors.general = 'Authentication error.'
          await this.$store.dispatch('auth/logout');
        } else {
          for (const key in this.errors) {
            if (result.errors.hasOwnProperty(key)) {
              this.errors[key] = result.errors[key];
            } else {
              this.errors[key] = null;
            }
          }
          this.submit = false;
        }
      }
      else {
        this.$router.push('/error')
      }
    }
  },
  computed: {
    ...mapState('auth', ['logged', 'collection'])
  },
  async created() {
    this.$watch(() => this.$route.params.book_id, this.fetchData, {
      immediate: true,
    });
  },
};
</script>

<style>
.book-container {
  display: flex;
  justify-content: space-between;
  gap: 30px;
  padding: 20px;
  min-height: 500px;
}

.disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
}

.img-card img {
  width: 90%;
  max-height: 60%;
  object-fit: contain;
  box-sizing: border-box;
  border-radius: 8px;
  padding-top: 30px;
  padding-bottom: 30px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid black
}

.book-info {
  width: 60%;
  display: flex;
  flex-direction: column;
}

.book-info h3 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 10px;
}

.book-meta {
  margin-bottom: 20px;
  margin-left: 4px;
}

.book-meta h5 {
  font-size: 20px;
  color: #333;
  margin-bottom: 5px;
}

.book-meta p {
  font-size: 16px;
  color: #666;
  margin: 5px 0;
}

.description {
  margin-bottom: 20px;
  margin-left: 4px;
}

.description b {
  font-size: 18px;
}

.description p {
  font-size: 16px;
  color: #333;
  line-height: 1.6;
}

.action-buttons button {
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.action-buttons button.primary {
  background-color: #007bff;
  color: #fff;
}

.action-buttons button.secondary {
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #333;
  margin-left: 10px;
}

.not-found {
  padding-top: 100px;
  font-size: 32px;
  text-align: center;
}
</style>
