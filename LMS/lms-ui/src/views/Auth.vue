<template>
  <section class="auth-container">
    <div class="auth-content">
      <h1>{{ title }}</h1>
      <h3>{{displayedMessage}}</h3>
      <div class="auth-form">
        <LoginForm v-if="formType === 'login'">
          <div class="auth-options">
            <div>new to LMS?<router-link to="/auth/register" replace>Register</router-link></div>
          </div>
        </LoginForm>
  
        <RegisterForm v-else-if="formType === 'register'" @message="displayMessage" >
          <div class="auth-options">
            <div>already have an account?<router-link to="/auth/login" replace>Login</router-link></div>
          </div>
        </RegisterForm>
        <UpdateUserForm v-else-if="formType === 'update-user'"></UpdateUserForm>
      </div>
      <i class="fa fa-close" aria-hidden="true" @click="close"></i>
    </div>
  </section>
</template>

<script>
import LoginForm from '@/components/forms/LoginForm.vue';
import RegisterForm from '@/components/forms/RegisterForm.vue';
import  UpdateUserForm  from "@/components/forms/UpdateUserForm.vue";
export default {
  name: 'AuthView',
  components: { RegisterForm, LoginForm, UpdateUserForm },

  data() {
    return {
      displayedMessage:null
    }

  },
  methods: {
    displayMessage(message) {
      this.displayedMessage = message;

      setTimeout(() => {
        this.displayedMessage = '';
      }, 2000);
    },
    close() {
      let to = this.$router.options.history.state.back;
      if(to){
        this.$router.replace(to)
      }else{
        this.$router.replace("/home");
      }      
    }
 
  },
  computed: {
    formType() {
      return this.$route.params.formType
    },
    title() {
      if (this.formType == "login") {
        return "User Login"
      }
      else if (this.formType == "update-user") {
        return "Update Profile"
      }
      else if (this.formType == "register") {
        return "Register"
      }

    }
  }
}

</script>

<style scoped>
.auth-content i:last-child {
  position: absolute;
  top: 7px;
  right: 10px;
  color: black;
  font-size: 25px;
  cursor: pointer;
  padding: 5px 7px;
  border: 2px solid black;
  border-radius: 50%;

}

.auth-content i:last-child:hover {
  transform: scale(0.9);
}
</style>
