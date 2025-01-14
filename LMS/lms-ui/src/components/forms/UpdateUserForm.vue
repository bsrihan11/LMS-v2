<template>
  <form @submit.prevent="handleUpdate">
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
    </div>
    <br>
    <button class="auth-button" type="submit" :disabled="submit">Update</button>
  </form>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import {
  emailValidation, required, nameValidation, lengthValidation
} from "@/utilities/utilities.js"
export default {
  name: 'UpdateUserForm',
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
        }
      },
      errors: {
        general: null,
        first_name: null,
        last_name: null,
        email: null
      }
    }
  },
  methods: {
    ...mapActions('auth', ['updateUser']),
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
    async handleUpdate() {
      this.submit = true;
      this.validate()
      if (this.validated) {
        let result = await this.updateUser({
          email: this.inputs.email.value,
          first_name: this.inputs.first_name.value,
          last_name: this.inputs.last_name.value
        });
        if (result === true) {
          let to = this.$router.options.history.state.back
          if (to) {
            this.$router.replace(to)
          } else {
            this.$router.replace('/home')
          }
        } else if (result) {
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

      }
    }
  },
  computed: {
    ...mapState('auth', ['logged', 'user'])
  },
  watch: {
    logged: {
      handler(newVal) {
        if (!newVal) {
          this.$router.replace('/home');
        }
      }
    },
    user: {
      handler(newUser) {
        if (newUser) {
          this.inputs.first_name.value = newUser.first_name;
          this.inputs.last_name.value = newUser.last_name;
          this.inputs.email.value = newUser.email;
        }
      },
      immediate: true
    }
  }
}
</script>
