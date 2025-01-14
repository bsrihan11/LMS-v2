<template>
  <div v-if="type === 'loading'" class="loading">
    Loading...
  </div>
  <div v-else-if="type === 'fetch'" class="crud-container">
    <h2 style="margin-bottom:30px;">Update User Priviliges</h2>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <form @submit.prevent="handleEmail">
      <input type="text" v-model.trim="email.value" placeholder="Enter User email"/>
      <br>
      <div v-if="errors.email" class="error">{{ errors.email }}</div>
      <br>
      <button type="submit" :disabled="submit">Get</button>
    </form>
  </div>
  <div v-else class="crud-container">
    <h2 style="margin-bottom:30px;">Update User Priviliges</h2>
    <button class="back-btn" @click="goBack()"><i class="fa-solid fa-arrow-left"></i></button>
    <div v-if="message" class="crud-message">{{ message }}</div>
    <div v-if="errors.general" class="error">{{ errors.general }}</div>
    <form @submit.prevent="handleUpdate">
      <div>
        <div>Name: <b>{{ user.first_name }} {{ user.last_name }}</b></div>
        <div>Email: <b>{{ user.email}}</b></div>
        <br>
        <br>
        <label>
          <b>Active: </b>
          <input type="checkbox" v-model="user.inputs.active.value" :checked="user.inputs.active.value" />
          <div v-if="errors.active" class="error">{{ errors.active }}</div>
        </label>
        <br>
        <br>
        <div v-if="errors.role" class="error">{{ errors.role }}</div>
        <div style="display:flex;flex-direction:row;align-items:center;">
          <label style="margin-right:5px;"><b>Role: </b></label>
          <select v-model="user.inputs.role.value" class="aduser-select-field">
            <option v-for="role in roles" :key="role.role_name" :value="role.role_id"
              :selected="role.role_id === user.inputs.role">{{ role.role_name }}</option>
          </select>
        </div>
        <br>
      </div>
      <br>
      <button type="submit" :disabled="submit">Update</button>
    </form>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import {
  emailValidation, required
} from "@/utilities/utilities.js"
export default {
  name: 'AdUpdateUser',
  data() {
    return {
      type: 'loading',
      validated: true,
      submit: false,
      roles: null,
      message:null,
      email: {
        value: null,
        validators: [{ func: required }, { func: emailValidation }]
      },

      user: {
        first_name: '',
        last_name: '',
        email: '',
        user_id: null,
        inputs: {
          active: {
            value: false,
            validators: []
          },
          role: {
            value: null,
            validators: []
          }
        }
      },
      errors: {
        general: null,
        role: null,
        active: null,
        email: null
      }
    }
  },
  methods: {
    ...mapActions('auth', ['getToken']),
    goBack(){

      this.reset_email();
      this.reset_user();
      this.type = 'options';
    },
    displayMessage(message) {
      this.message = message;

      setTimeout(() => {
        this.message = null;
      }, 5000);
    },
    reset_email() {
      this.email.value = ''
    },
    reset_user() {
      this.user.first_name = ''
      this.user.last_name = ''
      this.user.email = ''
      this.user.inputs.role.value = null
      this.user.inputs.active.value = false
      this.user.user_id = null

    },
    reset_error() {
      this.errors.general = null
      this.errors.role = null
      this.errors.active = null
      this.errors.email = null
    },
    validate() {
      let hasErrors = false;
      Object.entries(this.user.inputs).forEach(([name, field]) => {
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

      this.validated = !hasErrors
    },
    validateEmail() {
      let errorFound = false;
      for (const validator of this.email.validators) {
        let args = validator.args ? validator.args : []
        let result = validator.func(this.email.value, ...args);
        if (result !== true) {
          this.errors['email'] = result;
          errorFound = true;
          break;
        }
      }
      if (!errorFound) {
        this.errors['email'] = null;
      }
      this.validated = !errorFound
    },
    async handleEmail() {
      this.validateEmail();

      if (this.validated) {
        try {
          const csrf_access_token = await this.$store.dispatch('auth/getToken');
          const response = await fetch('http://localhost:5000/api/admin/get_user', {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrf_access_token
            },
            body: JSON.stringify({
              email: this.email.value
            }),
            credentials: 'include'
          })

          const data = await response.json()
          if (response.ok) {
            this.user.first_name = data.user.first_name
            this.user.last_name = data.user.last_name
            this.user.email = data.user.email
            this.user.inputs.role.value = data.user.role_id
            this.user.inputs.active.value = data.user.active === 1 ? true : false
            this.user.user_id = data.user.user_id
            this.submit = false;
            this.type = 'update'
            this.displayMessage('User fetched.')
            this.reset_email()
            this.reset_error()
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
          } else {
            this.errors['general'] = 'Internal error'
          }
        } catch (error) {
          console.error("Fetching user failed: ", error)
        }
      } else {
        this.submit = false;
      }
    },
    async handleUpdate() {
      this.validate()
      if (this.validated) {
        try {
          const csrf_access_token = await this.getToken()
          const response = await fetch('http://localhost:5000/api/admin/update_user', {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRF-TOKEN': csrf_access_token
            },
            body: JSON.stringify({
              user_id: this.user.user_id,
              role_id: this.user.inputs.role.value,
              active: this.user.inputs.active.value === true ? 1 : 0
            }),
            credentials: 'include'
          })

          const data = await response.json()
          if (response.ok) {
            this.submit = false;
            this.type = 'fetch'
            this.displayMessage(`User access updated for ${this.user.email}`)
            this.reset_user()
            this.reset_error()


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
            this.errors['general'] = 'Internal error'
          }
        } catch (error) {
          console.error('Updating user failed: ', error)
        }
      }
      else {
        this.submit = false;
      }

    }
  },
  computed: {
    ...mapState('master', ['admin'])
  },
  async created() {
    if (this.admin) {
      this.roles = this.admin.roles
      this.type = 'fetch'
    }
  },
  watch: {
    admin(newVal) {
      if (newVal) {
        this.roles = newVal.roles
        this.type = 'fetch'
      }
    }
  }
}

</script>

<style scoped>
.aduser-form-container {
  margin: 50px;
  text-align: center;
  width: 50%;
  margin: 0 auto;
  margin-top: 50px;
  border: 1px solid black;
  padding: 25px 17px;
  background: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 30px;
}

.aduser-form {
  width: 300px;
  margin: auto;
}

.aduser-input-field {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.aduser-select-field {
  width: 80%;
  padding: 5px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s ease;
  font-size: 16px;
  color: #333;
}

.aduser-submit-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.aduser-error {
  color: red;
  margin-top: 5px;
}

.aduser-loading {
  font-size: 20px;
  text-align: center;
  margin-top: 50px;
}
</style>