<template>
  <div class="crud-container" v-if="type === 'options'">
    <h1>Author CRUD</h1>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <br>
    <button @click="type = 'create' " class="create-button"><i class="fas fa-plus icon"></i>Create</button>
    <br>
    <div style="color:grey; font-size:25px">or</div>
    <br>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <input type="number" v-model="author_id.value" placeholder="Enter author ID">
    <div v-if="errors.author_id" class="error">{{ errors.author_id }}</div>
    <button @click="read_author()" :disabled='submit' class="get-button"><i class="fas fa-eye icon"></i>Get</button>
  </div>
  <div class="crud-container" v-else-if="type === 'update'">
    <h1>Author CRUD</h1>
    <button class="back-btn" @click="goBack()"><i class="fa-solid fa-arrow-left"></i></button>
    
    <div v-if="message" class="crud-message">{{ message }}</div>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <form @submit.prevent="update_author()">
      <div>
        <label for="author_name">Author Name:</label>
        <input type="text" v-model="author.author_name.value">
        <div v-if="errors.author_name" class="error">{{ errors.author_name }}</div>
      </div>
      <div style="display:flex;align-items:center;justify-content:space-around;">
        <button type="submit" :disabled="submit" @click="action='edit'">Update</button>
        <button type="submit" :disabled="submit" @click="action='delete'">Delete</button>
      </div>
      <br>
    </form>
  </div>
  <div class="crud-container" v-else>
    <h1>Author CRUD</h1>
    <button class="back-btn" @click="goBack()"><i class="fa-solid fa-arrow-left"></i></button>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <form @submit.prevent="create_author()">
      <div>
        <label for="author_name">Author Name:</label>
        <input type="text" v-model="author.author_name.value">
        <div v-if="errors.author_name" class="error">{{ errors.author_name }}</div>
      </div>
  
      <br>
      <button type="submit" :disabled="submit">Create Author</button>
    </form>
  
  </div>
</template>

<script>
import {
  required, lengthValidation, imageValidation
} from "@/utilities/utilities.js";
export default {
  name: 'AuthorCRUD',
  data() {
    return {
      type: 'options',
      submit: false,
      message: null,
      action: null,
      id_validated: true,
      validated: true,
      author_id: {
        value: null,
        validators: [{ func: required }]
      },
      author: {
        author_name: {
          value: '',
          validators: [{ func: required }, { func: lengthValidation, args: [1, 264] }]
        }
      },
      errors: {
        author_name: null,
        general: null,
        author_id: null
      }
    }
  },
  computed: {
  },
  methods: {
    goBack(){

      this.reset_author();
      this.reset_author_id();
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
      for (const validator of this.author_id.validators) {
        let args = validator.args ? validator.args : []
        let result = validator.func(this.author_id.value, ...args);
        if (result !== true) {
          this.errors['author_id'] = result;
          errorFound = true;
          break;
        }
      }
      if (!errorFound) {
        this.errors['author_id'] = null;
      }
      this.id_validated = !errorFound
    },
    validate_author() {
      let hasErrors = false;
      Object.entries(this.author).forEach(([name, field]) => {
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
    populate_author(fetched_author) {
      Object.keys(this.author).forEach(key => {
        if (fetched_author.hasOwnProperty(key)) {
          this.author[key].value = fetched_author[key]
        }
      });
    },
    reset_author_id() {
      this.author_id.value = null;
      this.errors.author_id = null;
    },
    reset_author() {
      for (let key in this.author) {
        if (this.author.hasOwnProperty(key)) {
          switch (key) {
            case 'author_name':
              this.author[key].value = '';
              break;
          }
        }
      }
    },
    async read_author() {
      this.submit = true;
      this.validate_id();
      if (this.id_validated) {
        const response = await fetch(`http://localhost:5000/api/author/${this.author_id.value}`, {
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
          this.displayMessage('You can now modify author.')
          this.populate_author(data.author);
        }
        else if (response.status === 404) {
          this.displayMessage('Invalid Author.')
          this.submit = false;
        }
        else {
          this.displayMessage('Error fetching author.')
          this.submit = false;
        }
      }
      else {
        this.submit = false;
      }
    },

    async edit_author() {
      this.validate_author();
      if (this.validated) {
        const csrf_access_token = await this.$store.dispatch('auth/getToken');
        const response = await fetch(`http://localhost:5000/api/author/${this.author_id.value}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf_access_token
          },
          body: JSON.stringify({
            author_name: this.author.author_name.value
          }),
          credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
          this.displayMessage(`Author with ID ${this.author_id.value} successfully updated.`)
          this.reset_author();
          this.reset_author_id();
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
          this.displayMessage('Error updating author.')
          this.submit = false;
        }
      }
      else {
        this.submit = false;
      }

    },

    async delete_author() {
      const csrf_access_token = await this.$store.dispatch('auth/getToken');
      const response = await fetch(`http://localhost:5000/api/author/${this.author_id.value}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf_access_token
        },
        credentials: 'include'
      });

      if (response.ok) {
        this.displayMessage(`Author with ID ${this.author_id.value} successfully deleted.`)
        this.reset_author();
        this.reset_author_id();
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
        this.displayMessage('Error deleting author.')
        this.submit = false;
      }


    },
    async update_author() {
      this.submit = true;
      if (this.action === 'edit') {
        this.edit_author()
      }
      else if (this.action === 'delete') {
        this.delete_author()
      }
      else {
        this.submit = false;
      }
    },
    async create_author() {
      this.submit = true;
      this.validate_author();
      if (this.validated) {
        const csrf_access_token = await this.$store.dispatch('auth/getToken');
        const response = await fetch(`http://localhost:5000/api/author`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf_access_token
          },
          body: JSON.stringify({
            author_name: this.author.author_name.value

          }),
          credentials: 'include'
        });

        const data = await response.json();
        if (response.ok) {
          this.displayMessage(`Author successfully created with ID:${data.author_id}`)
          this.reset_author();
          this.reset_author_id();
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
          this.displayMessage('Error creating author.')
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