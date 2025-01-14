<template>
  <section class="auth-container">
    <div class="auth-content">
      <h1>Master Login</h1>
      <div class="auth-form">
        <form @submit.prevent="handleLogin">
          <div class="auth-input">
            <div v-if="errors.general" class="error">{{ errors.general }}</div>
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
      </div>
    </div>
  </section>
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
          let role = this.user.role;
          if(role === 'USER'){
            this.errors['general'] = 'Access Denied.Only for Master use.';
          }
          else{
            if(role === 'ADMIN'){
              this.$router.replace('/master/admin/dashboard')
            }
            else{
              this.$router.replace('/master/manager/book')
            }
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
    }
  },
  computed: {
    ...mapState('auth', ['user'])
  }

};
</script>
