<template>
  <div class="crud-container" v-if="type === 'options'">
    <h1>Book CRUD</h1>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <br>
    <button @click="type = 'create' " class="create-button"><i class="fas fa-plus icon"></i>Create</button>
    <!-- Create button -->
    <br>
    <div style="color:grey; font-size:25px">or</div>
    <br>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <input type="number" v-model="book_id.value" placeholder="Enter book ID">
    <div v-if="errors.book_id" class="error">{{ errors.book_id }}</div>
    <button @click="read_book()" :disabled='submit' class="get-button"><i class="fas fa-eye icon"></i>Get</button>
  </div>
  <div class="crud-container" v-else-if="type === 'update'">
    <h1>Book CRUD</h1>
    <button class="back-btn" @click="goBack()"><i class="fa-solid fa-arrow-left"></i></button>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <form @submit.prevent="update_book()">
      <div>
        <label for="book_name">Book Name:</label>
        <input type="text" v-model="book.book_name.value">
        <div v-if="errors.book_name" class="error">{{ errors.book_name }}</div>
      </div>
      <div>
        <label for="book_cover">Book Cover:</label>
        <input type="text" v-model="book.book_cover.value">
        <div v-if="errors.book_cover" class="error">{{ errors.book_cover }}</div>
      </div>
      <div>
        <label for="book_price">Book Price:</label>
        <input type="number" v-model="book.book_price.value">
        <div v-if="errors.book_price" class="error">{{ errors.book_price }}</div>
      </div>
      <div>
        <label for="section_id">Section ID:</label>
        <input type="number" v-model="book.section_id.value">
        <div v-if="errors.section_id" class="error">{{ errors.section_id }}</div>
      </div>
      <div>
        <label for="path">Path:</label>
        <input type="text" v-model="book.path.value">
        <div v-if="errors.path" class="error">{{ errors.path }}</div>
      </div>
      <div>
        <label for="book_summary">Book Summary:</label>
        <textarea v-model="book.book_summary.value"></textarea>
        <div v-if="errors.book_summary" class="error">{{ errors.book_summary }}</div>
      </div>
      <div>
        <label for="year">Year:</label>
        <input type="number" v-model="book.year.value">
        <div v-if="errors.year" class="error">{{ errors.year }}</div>
      </div>
      <div>
        <label for="days">Days:</label>
        <input type="number" v-model="book.days.value">
        <div v-if="errors.days" class="error">{{ errors.days }}</div>
      </div>
      <div>
        <label for="author_list">Authors:</label>
        <input type="text" v-model="book.author_list.value">
        <div v-if="errors.author_list" class="error">{{ errors.author_list }}</div>
      </div>
      <div>
        <label for="is_available">Is Available:</label>
        <input type="checkbox" v-model="book.is_available.value">
        <div v-if="errors.is_available" class="error">{{ errors.is_available }}</div>
      </div>
      <button type="submit" :disabled="submit">Update Book</button>
    </form>
  </div>
  <div class="crud-container" v-else>
    <h1>Book CRUD</h1>
    <button class="back-btn" @click="goBack()"><i class="fa-solid fa-arrow-left"></i></button>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <form @submit.prevent="create_book()">
      <div>
        <label for="book_name">Book Name:</label>
        <input type="text" v-model="book.book_name.value">
        <div v-if="errors.book_name" class="error">{{ errors.book_name }}</div>
      </div>
      <div>
        <label for="book_cover">Book Cover:</label>
        <input type="text" v-model="book.book_cover.value">
        <div v-if="errors.book_cover" class="error">{{ errors.book_cover }}</div>
      </div>
      <div>
        <label for="book_price">Book Price:</label>
        <input type="number" v-model="book.book_price.value">
        <div v-if="errors.book_price" class="error">{{ errors.book_price }}</div>
      </div>
      <div>
        <label for="section_id">Section ID:</label>
        <input type="number" v-model="book.section_id.value">
        <div v-if="errors.section_id" class="error">{{ errors.section_id }}</div>
      </div>
      <div>
        <label for="path">Path:</label>
        <input type="text" v-model="book.path.value">
        <div v-if="errors.path" class="error">{{ errors.path }}</div>
      </div>
      <div>
        <label for="book_summary">Book Summary:</label>
        <textarea v-model="book.book_summary.value"></textarea>
        <div v-if="errors.book_summary" class="error">{{ errors.book_summary }}</div>
      </div>
      <div>
        <label for="year">Year:</label>
        <input type="number" v-model="book.year.value">
        <div v-if="errors.year" class="error">{{ errors.year }}</div>
      </div>
      <div>
        <label for="days">Days:</label>
        <input type="number" v-model="book.days.value">
        <div v-if="errors.days" class="error">{{ errors.days }}</div>
      </div>
      <div>
        <label for="author_list">Authors:</label>
        <input type="text" v-model="book.author_list.value">
        <div v-if="errors.author_list" class="error">{{ errors.author_list }}</div>
      </div>
      <div>
        <label for="is_available">Is Available:</label>
        <input type="checkbox" v-model="book.is_available.value">
        <div v-if="errors.is_available" class="error">{{ errors.is_available }}</div>
      </div>
      <button type="submit" :disabled="submit">Create Book</button>
    </form>
  
  </div>
</template>

<script>
import {
  required, lengthValidation, pdfValidation, imageValidation, authorValidation
} from "@/utilities/utilities.js"
import { mapActions } from 'vuex';
export default {
  name: 'BookCRUD',
  data() {
    return {
      type: 'options',
      submit: false,
      message: null,
      id_validated: true,
      validated: true,
      book_id: {
        value: null,
        validators: [{ func: required }]
      },
      book: {
        book_name: {
          value: '',
          validators: [{ func: required }, { func: lengthValidation, args: [1, 264] }]
        },
        book_cover: {
          value: '',
          validators: [{ func: required }, { func: lengthValidation, args: [1, 100] }, { func: imageValidation }]
        },
        book_price: {
          value: null,
          validators: [{ func: required }]
        },
        section_id: {
          value: null,
          validators: [{ func: required }]
        },
        path: {
          value: '',
          validators: [{ func: required }, { func: lengthValidation, args: [1, 200] }, { func: pdfValidation }]
        },
        book_summary: {
          value: '',
          validators: [{ func: required }, { func: lengthValidation, args: [30, 300] }]
        },
        year: {
          value: null,
          validators: [{ func: required }]

        },
        days: {
          value: null,
          validators: [{ func: required }]
        },
        author_list: {
          value: null,
          validators: [{ func: required }, { func: authorValidation }]
        },
        is_available: {
          value: false,
          validators: []
        }
      },
      errors: {
        book_name: null,
        book_cover: null,
        book_price: null,
        book_summary: null,
        section_id: null,
        path: null,
        is_available: null,
        days: null,
        year: null,
        general: null,
        book_id: null,
        author_list: null

      }

    }
  },
  computed: {
  },
  methods: {
    goBack(){

      this.reset_book();
      this.reset_book_id();
      this.type = 'options';
    },
    displayMessage(message) {
      this.message = message;

      setTimeout(() => {
        this.message = null;
      }, 8000);
    },
    validate_id() {
      let errorFound = false;
      for (const validator of this.book_id.validators) {
        let args = validator.args ? validator.args : []
        let result = validator.func(this.book_id.value, ...args);
        if (result !== true) {
          this.errors['book_id'] = result;
          errorFound = true;
          break;
        }
      }
      if (!errorFound) {
        this.errors['book_id'] = null;
      }
      this.id_validated = !errorFound
    },
    validate_book() {
      let hasErrors = false;
      Object.entries(this.book).forEach(([name, field]) => {
        let errorFound = false;
        for (const validator of field.validators) {
          let args = validator.args ? validator.args : []
          let result = validator.func(field.value, ...args);
          if (result !== true) {
            this.errors[name] = result;
            errorFound = true;
            hasErrors = true;
            break;
          } else {
            this.errors[name] = null;
          }
        }
        if (!errorFound) {
          this.errors[name] = null;
        }
      });

      this.validated = !hasErrors;
    },
    populate_book(fetched_book) {
      Object.keys(this.book).forEach(key => {
        if (fetched_book.hasOwnProperty(key)) {
          this.book[key].value = fetched_book[key]
        }
      })
    },
    reset_book_id() {
      this.book_id.value = null;
      this.errors.book_id = null;
    },
    reset_book() {
      for (let key in this.book) {
        if (this.book.hasOwnProperty(key)) {
          switch (key) {
            case 'book_name':
            case 'book_cover':
            case 'path':
            case 'book_summary':
              this.book[key].value = '';
              break;
            case 'year':
            case 'book_price':
            case 'days':
            case 'section_id':
              this.book[key].value = null;
              break;
            case 'is_available':
              this.book[key].value = false;
              break;
          }
        }
      }
    },
    async read_book() {
      this.submit = true;
      this.validate_id();
      if (this.id_validated) {
        const response = await fetch(`http://localhost:5000/api/book/${this.book_id.value}?type=ADMIN`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include'
        });

        const data = await response.json()
        if (response.ok) {
          this.type = 'update'
          this.submit = false;
          this.displayMessage('You can now modify book.')
          this.populate_book(data.book);
        }
        else if (response.status === 404) {
          this.displayMessage('Invalid Book.')
          this.submit = false;
        }
        else {
          this.displayMessage('Error fetching book.')
          this.submit = false;
        }
      }
      else {
        this.submit = false;
      }
    },
    async update_book() {
      this.submit = true;
      this.validate_book();
      if (this.validated) {
        const csrf_access_token = await this.$store.dispatch('auth/getToken');
        const response = await fetch(`http://localhost:5000/api/book/${this.book_id.value}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf_access_token
          },
          body: JSON.stringify({
            book_name: this.book.book_name.value,
            book_cover: this.book.book_cover.value,
            book_price: this.book.book_price.value,
            book_summary: this.book.book_summary.value,
            section_id: this.book.section_id.value,
            path: this.book.path.value,
            is_available: this.book.is_available.value,
            days: this.book.days.value,
            year: this.book.year.value,
            author_list: this.book.author_list.value

          }),
          credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
          this.displayMessage(`Book with ID ${this.book_id.value} successfully updated.`)
          this.reset_book();
          this.reset_book_id();
          this.type = 'options';
          this.submit = false;
        }
        else if (response.status === 401 || response.status === 404) {
          if (data.msg) {
            await this.$store.dispatch('auth/logout');
            this.$router.replace('/master/login');
          }
          else {
            for (const key in this.errors) {
              if (data.errors.hasOwnProperty(key)) {
                this.errors[key] = data.errors[key];
              }
              else {
                this.errors[key] = null;
              }
            }
            this.submit = false
          }
        }
        else {
          this.displayMessage('Error updating book.')
          this.submit = false;
        }
      }
      else {
        this.submit = false;
      }
    },
    async create_book() {
      this.submit = true;
      this.validate_book();
      if (this.validated) {
        const csrf_access_token = await this.$store.dispatch('auth/getToken');
        const response = await fetch(`http://localhost:5000/api/book`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf_access_token
          },
          body: JSON.stringify({
            book_name: this.book.book_name.value,
            book_cover: this.book.book_cover.value,
            book_price: this.book.book_price.value,
            book_summary: this.book.book_summary.value,
            section_id: this.book.section_id.value,
            path: this.book.path.value,
            is_available: this.book.is_available.value,
            days: this.book.days.value,
            year: this.book.year.value,
            author_list: this.book.author_list.value

          }),
          credentials: 'include'
        });

        const data = await response.json();
        if (response.ok) {
          this.displayMessage(`Book successfully created with ID:${data.book_id}`)
          this.reset_book();
          this.reset_book_id();
          this.type = 'options';
          this.submit = false;
        }
        else if (response.status === 401) {
          if (data.msg) {
            await this.$store.dispatch('auth/logout');
            this.$router.replace('/master/login');
          }
          else {
            for (const key in this.errors) {
              if (data.errors.hasOwnProperty(key)) {
                this.errors[key] = data.errors[key];
              }
              else {
                this.errors[key] = null;
              }
            }
            this.submit = false
          }
        }
        else {
          this.displayMessage('Error creating book.')
          this.submit = false;
        }
      }
      else {
        this.submit = false;
      }
    }
  }
}
</script>

