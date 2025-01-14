<template>
  <form @submit.prevent="handleRegistration">
    <div class="auth-input">
      <div v-if="errors.general" class="error" style="text-align:center;">{{ errors.general }}</div>
      <input v-model.trim="inputs.first_name.value" placeholder="Enter your First Name" />
      <div v-if="errors.first_name" class="error">{{ errors.first_name }}</div>
      <br>
      <input v-model.trim="inputs.last_name.value" placeholder="Enter your Last Name" />
      <div v-if="errors.last_name" class="error">{{ errors.last_name }}</div>
      <br>
      <input v-model.trim="inputs.email.value" placeholder="Enter your email" />
      <div v-if="errors.email" class="error">{{ errors.email }}</div>
      <br>
      <input type="password" v-model.trim="inputs.password.value" placeholder="Your password" />
      <div v-if="errors.password" class="error">{{ errors.password }}</div>
    </div>
    <br>
    <button class="auth-button" type="submit" :disabled="submit">Register</button>
    <slot></slot>
  </form>
</template>

<script>
import {mapActions,mapState} from 'vuex';
import {
  emailValidation, passwordValidation, required, nameValidation, lengthValidation
} from "@/utilities/utilities.js"
export default {
  name: 'RegisterForm',
  data() {
    return {
      validated: true,
      submit: false,
      inputs: {
        first_name: {
          value: '',
          validators: [

            { func: required },
            { func: lengthValidation, args: [1, 50] },
            { func: nameValidation }
          ]
        },
        last_name: {
          value: '',
          validators: [
            { func: required },
            { func: lengthValidation, args: [1, 50] },
            { func: nameValidation }
          ]
        },
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
        first_name: null,
        last_name: null,
        email: null,
        password: null
      }
    }
  },
  methods: {
    ...mapActions('auth', ['register']),
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

      this.validated = !hasErrors;
    },
    async handleRegistration() {
      this.submit = true;
      this.validate()
      if (this.validated) {
        let result = await this.register({
          email: this.inputs.email.value,
          password: this.inputs.password.value,
          first_name:this.inputs.first_name.value,
          last_name:this.inputs.last_name.value
        });
        if (result === true) {
          this.$router.replace('/auth/login')
          this.$emit('message', 'Registration successful,You can now login.');
        }else {
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
    ...mapState('auth', ['logged'])
  },
  mounted() {
    if (this.logged) {
      this.$router.replace('/home')
    }
  }
}
</script>
