<template>
  <div class="crud-container" v-if="type === 'options'">
    <h1>Section CRUD</h1>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <br>
    <button @click="type = 'create'" class="create-button"><i class="fas fa-plus icon"></i>Create</button>
    <br>
    <div style="color:grey; font-size:25px">or</div>
    <br>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <input type="number" v-model="section_id.value" placeholder="Enter section ID">
    <div v-if="errors.section_id" class="error">{{ errors.section_id }}</div>
    <button @click="read_section()" :disabled='submit' class="get-button"><i class="fas fa-eye icon"></i>Get</button>
  </div>
  <div class="crud-container" v-else-if="type === 'update'">
    <h1>Section CRUD</h1>
    <button class="back-btn" @click="goBack()"><i class="fa-solid fa-arrow-left"></i></button>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <form @submit.prevent="update_section()">
      <div>
        <label for="section_name">Section Name:</label>
        <input type="text" v-model="section.section_name.value">
        <div v-if="errors.section_name" class="error">{{ errors.section_name }}</div>
      </div>
      <div>
        <label for="section_cover">Section Cover:</label>
        <input type="text" v-model="section.section_cover.value">
        <div v-if="errors.section_cover" class="error">{{ errors.section_cover }}</div>
      </div>
      <div style="display:flex;align-items:center;justify-content:space-around;">
        <button type="submit" :disabled="submit" @click="action='edit'">Update</button>
        <button type="submit" :disabled="submit" @click="action='delete'">Delete</button>
      </div>
    </form>
  </div>
  <div class="crud-container" v-else>
    <h1>Section CRUD</h1>
    <button class="back-btn" @click="goBack()"><i class="fa-solid fa-arrow-left"></i></button>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <form @submit.prevent="create_section()">
      <div>
        <label for="section_name">Section Name:</label>
        <input type="text" v-model="section.section_name.value">
        <div v-if="errors.section_name" class="error">{{ errors.section_name }}</div>
      </div>
      <div>
        <label for="section_cover">Section Cover:</label>
        <input type="text" v-model="section.section_cover.value">
        <div v-if="errors.section_cover" class="error">{{ errors.section_cover }}</div>
      </div>
      <br>
      <button type="submit" :disabled="submit">Create Section</button>
    </form>
  
  </div>
</template>

<script>
import {
  required, lengthValidation, imageValidation
} from "@/utilities/utilities.js";
export default {
  name: 'SectionCRUD',
  data() {
    return {
      type: 'options',
      submit: false,
      message: null,
      action: null,
      id_validated: true,
      validated: true,
      section_id: {
        value: null,
        validators: [{ func: required }]
      },
      section: {
        section_name: {
          value: '',
          validators: [{ func: required }, { func: lengthValidation, args: [1, 264] }]
        },
        section_cover: {
          value: '',
          validators: [{ func: required }, { func: lengthValidation, args: [1, 100] }, { func: imageValidation }]
        }
      },
      errors: {
        section_name: null,
        section_cover: null,
        general: null,
        section_id: null

      }

    }
  },
  computed: {
  },
  methods: {
    goBack(){

      this.reset_section();
      this.reset_section_id();
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
      for (const validator of this.section_id.validators) {
        let args = validator.args ? validator.args : []
        let result = validator.func(this.section_id.value, ...args);
        if (result !== true) {
          this.errors['section_id'] = result;
          errorFound = true;
          break;
        }
      }
      if (!errorFound) {
        this.errors['section_id'] = null;
      }
      this.id_validated = !errorFound
    },
    validate_section() {
      let hasErrors = false;
      Object.entries(this.section).forEach(([name, field]) => {
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
    populate_section(fetched_section) {
      Object.keys(this.section).forEach(key => {
        if (fetched_section.hasOwnProperty(key)) {
          this.section[key].value = fetched_section[key]
        }
      })
    },
    reset_section_id() {
      this.section_id.value = null;
      this.errors.section_id = null;
    },
    reset_section() {
      for (let key in this.section) {
        if (this.section.hasOwnProperty(key)) {
          switch (key) {
            case 'section_name':
            case 'section_cover':
              this.section[key].value = '';
              break;
          }
        }
      }
    },
    async read_section() {
      this.submit = true;
      this.validate_id();
      if (this.id_validated) {
        const response = await fetch(`http://localhost:5000/api/section/${this.section_id.value}?type=BRIEF`, {
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
          this.displayMessage('You can now modify section.')
          this.populate_section(data.section);

        }
        else if (response.status === 404) {
          this.displayMessage('Invalid Section.')
          this.submit = false;
        }
        else {
          this.displayMessage('Error fetching section.')
          this.submit = false;
        }
      }
      else {
        this.submit = false;
      }
    },

    async edit_section() {
      this.validate_section();
      if (this.validated) {
        const csrf_access_token = await this.$store.dispatch('auth/getToken');
        const response = await fetch(`http://localhost:5000/api/section/${this.section_id.value}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf_access_token
          },
          body: JSON.stringify({
            section_name: this.section.section_name.value,
            section_cover: this.section.section_cover.value
          }),
          credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
          this.displayMessage(`Section with ID ${this.section_id.value} successfully updated.`)
          this.reset_section();
          this.reset_section_id();
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
          this.displayMessage('Error updating section.')
          this.submit = false;
        }
      }
      else {
        this.submit = false;
      }

    },

    async delete_section() {
      const csrf_access_token = await this.$store.dispatch('auth/getToken');
      const response = await fetch(`http://localhost:5000/api/section/${this.section_id.value}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-TOKEN': csrf_access_token
        },
        credentials: 'include'
      });

      if (response.ok) {
        this.displayMessage(`Section with ID ${this.section_id.value} successfully deleted.`)
        this.reset_section();
        this.reset_section_id();
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
        this.displayMessage('Error deleting section.')
        this.submit = false;
      }


    },
    async update_section() {
      this.submit = true;
      if (this.action === 'edit') {
        this.edit_section()
      }
      else if (this.action === 'delete') {
        this.delete_section()
      }
      else {
        this.submit = false;
      }
    },
    async create_section() {
      this.submit = true;
      this.validate_section();
      if (this.validated) {
        const csrf_access_token = await this.$store.dispatch('auth/getToken');
        const response = await fetch(`http://localhost:5000/api/section`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf_access_token
          },
          body: JSON.stringify({
            section_name: this.section.section_name.value,
            section_cover: this.section.section_cover.value

          }),
          credentials: 'include'
        });

        const data = await response.json();
        if (response.ok) {
          this.displayMessage(`Section successfully created with ID:${data.section_id}`)
          this.reset_section();
          this.reset_section_id();
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
          this.displayMessage('Error creating section.')
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

