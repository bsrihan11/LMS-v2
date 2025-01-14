<template>
  <div class="collection-card">
    <div class="collection-info">
      <h3>{{ book.book_name }}</h3>
      <p class="deadline">{{ book.deadline }}</p>
    </div>
    <div class="collection-actions">
      <button @click="returnBook" :disabled="submit">Return</button>
      <div><b>Read: </b>
          <button class="fas fa-book-reader" @click="openPDF(book.book_id)"></button>
          </div>
      <div><b>Download: </b><button :class="{'fa-solid':true,'fa-download':!downloading,'fa-spinner':downloading}"
          @click="download" :disabled="downloading"></button></div>
  
      <div class="collection-rating">
        <div class="rating">
          <div v-for="star in totalStars" :key="star" @click="setRating(star)"
            :class="{ 'filled': star <= currentRating }" :style="{ 'pointer-events': disabled ? 'none' : 'auto' }">
            <span class="star"><i class="fa-solid fa-star"></i></span>
          </div>
          <button v-if="disabled" @click="disabled=!disabled">edit</button>
          <button v-if="!disabled" @click="saveRating()" style="background-color: #ad8018;">save</button>
        </div>
      </div>
    </div>
    <div v-if="errors.general" class="collection-error">{{errors.general}}</div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: "CollectionCard",
  props: {
    book: {
      type: Object,
      required: true
    },
    id: {
      required: true
    }
  },
  data() {
    return {
      currentRating: this.book.rating,
      totalStars: 5,
      downloading: false,
      submit: false,
      disabled: true,
      errors: {
        general: null
      }
    };
  },
  methods: {
    ...mapActions('auth', ['getToken', 'loadUser']),
    hideErrorMessage() {
      setTimeout(() => {
        this.errors.general = null;
      }, 5000);
    },
    openPDF(book_id){
      this.$router.push({ name: 'pdf_view', params: { book_id:book_id } })
    },
    async download() {
      const csrf_access_token = await this.getToken();
      this.downloading = true;
      const response = await fetch(`http://localhost:5000/api/transaction?book_id=${this.id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf_access_token
        },
        credentials: 'include'
      });


      if (response.ok) {
        const blob = await response.blob();
        const a = document.createElement('a');
        a.href = window.URL.createObjectURL(blob);
        a.download = this.book.book_name + ".pdf"
        document.body.appendChild(a);

        a.click();
        this.downloading = false;

      }
      else if (response.status === 401 || response.status === 404) {
        const result = await response.json();
        if (result.msg) {
          this.errors.general = 'Authentication Error.'
          await this.$store.dispatch('auth/logout');
        }
        else {
          for (const key in this.errors) {
            if (result.errors.hasOwnProperty(key)) {
              this.errors[key] = result.errors[key];
            }
            else {
              this.errors[key] = null;
            }
          }
          this.downloading = false;
        }
      }
      else {
        this.$router.push('/error')
      }

    },
    async returnBook() {
      this.submit = true;
      const csrf_access_token = await this.getToken();
      const response = await fetch(`http://localhost:5000/api/transaction?book_id=${this.id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf_access_token
        },
        credentials: 'include'
      });

      const result = await response.json();
      if (response.ok) {
        this.$store.dispatch('auth/return_book', this.id);
        this.submit = false;

      }
      else if (response.status === 401 || response.status === 404) {
        if (result.msg) {
          this.errors.general = 'Authentication Error.'
          await this.$store.dispatch('auth/logout');
        }
        else {
          for (const key in this.errors) {
            if (result.errors.hasOwnProperty(key)) {
              this.errors[key] = result.errors[key];
            }
            else {
              this.errors[key] = null;
            }

            this.submit = false;
          }
        }
      }
      else {
        this.$router.push('/error')
      }

    },
    async setRating(rating) {
      if (!this.disabled) {
        this.currentRating = rating;
      }
    },
    async saveRating() {
      if (!this.disabled) {
        try {
          const params = new URLSearchParams({ book_id: this.id, rating: this.currentRating });
          const url = `http://localhost:5000/api/rating?${params.toString()}`
          const csrf_access_token = await this.getToken();
          const response = await fetch(url, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrf_access_token
            },
            credentials: 'include',
            body: JSON.stringify({})
          });

          const result = await response.json();
          if (response.ok) {

            this.disabled = true;
            let payload = { book_id: this.id, rating: this.currentRating }
            this.$store.dispatch('auth/update_rating', payload);
          }
          else if (response.status === 401 || response.status === 404) {
            if (result.msg) {
              this.errors.general = 'Authentication Error.'
              await this.$store.dispatch('auth/logout');
            } else {
              for (const key in this.errors) {
                if (result.errors.hasOwnProperty(key)) {
                  this.errors[key] = result.errors[key];
                }
                else {
                  this.errors[key] = null;
                }
              }
              this.submit = false;
            }
          }
          else {
            this.$router.push('/error')
          }
        } catch (error) {
          console.error(error)
        }
      }
    },
  },
  watch: {
    'errors.general': {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.hideErrorMessage();
        }
      }
    }
  }
};
</script>

<style>
.collection-card {
  width: 80%;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.collection-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.deadline {
  color: #ff5a5f;
  font-weight: bold;
}

.collection-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.collection-actions button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
}

.collection-actions button:hover {
  transform: scale(0.95);
}

.collection-rating {
  align-self: center;
  display: flex;
  flex-direction: column;
  margin-top: 10px;
}

.rating {
  display: flex;
  align-items: center;
}

.rating button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  margin-left: 10px;
}

.star {
  font-size: 24px;
  cursor: pointer;
}

.filled {
  color: gold;
}

.rating button.edit:hover {
  background-color: #ad8018;
}

.fa-spinner {
  animation: spin 1s linear infinite;
}

.collection-error {
  width: 80%;
  text-align: center;
  background-color: #f8d7da;
  color: #721c24;
  border-radius: 5px;
  margin: 7px auto;
}
</style>