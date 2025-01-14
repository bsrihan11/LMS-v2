<template>
  <form @submit.prevent="handleLogin">
    <div class="auth-input">
      <div v-if="errors.general" class="error" style="text-align:center;">{{ errors.general }}</div>
      <input v-model.trim="inputs.email.value" placeholder="Enter your email" />
      <div v-if="errors.email" class="error">{{ errors.email }}</div>
      <br>
      <input type="password" v-model.trim="inputs.password.value" placeholder="Your password" />
      <div v-if="errors.password" class="error">{{ errors.password }}</div>
    </div>
    <br>
    <button class="auth-button" type="submit" :disabled="submit">Login</button>
    <slot></slot>
  </form>
</template>

<script>

import {
  emailValidation, passwordValidation, required
} from "@/utilities/utilities.js"
import { mapActions, mapState } from 'vuex';
export default {
  name: 'LoginForm',
  data() {
    return {
      validated: true,
      submit: false,
      inputs: {
        email: {
          value: '',
          validators: [
            { func: required },
            { func: emailValidation }
          ]
        },
        password: {
          value: '',
          validators: [
            { func: required },
            { func: passwordValidation }
          ]
        },
      },
      errors: {
        general: null,
        email: null,

        password: null
      }
    }
  },
  methods: {
    ...mapActions('auth', ['login']),
    validate() {
      let hasErrors = false;
      Object.entries(this.inputs).forEach(([name, field]) => {
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
    async handleLogin() {
      this.submit = true;
      this.validate()
      if (this.validated) {
        let result = await this.login({
          email: this.inputs.email.value,
          password: this.inputs.password.value
        });
        if (result == true) {

          let to = this.$router.options.history.state.back
          if (to) {
            this.$router.replace(to)
          } else {
            this.$router.replace('/home')
          }
        }
        else {
          for (const key in this.errors) {
            if (result.hasOwnProperty(key)) {
              this.errors[key] = result[key];
            }
            else {
              this.errors[key] = null;
            }
          }
          this.submit = false;
        }

      } else {
        this.submit = false;
        console.log('Failure')
      }
    },
    // async login()
  },
  computed: {
    ...mapState('auth', ['user'])
  }
}
</script>

