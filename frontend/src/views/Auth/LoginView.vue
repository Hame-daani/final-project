// src/views/Login.vue

<template>
  <div>
    <h1>Login</h1>
    <input type="text" placeholder="Username" v-model="username" />
    <input type="text" placeholder="Password" v-model="password" />
    <input type="button" @click="login" value="Login" />
    <div v-if="errors">
      <p v-for="error in errors" v-bind:key="error">
        {{ error }}
      </p>
    </div>
  </div>
</template>
<script>
import AuthService from "@/services/AuthService.js";

export default {
  data() {
    return {
      username: "",
      password: "",
      errors: [],
    };
  },
  methods: {
    async login() {
      try {
        const credentials = {
          username: this.username,
          password: this.password,
        };
        const response = await AuthService.login(credentials);
        const token = response.token;
        const user = response.user;

        this.$store.dispatch("auth/login", { token, user });

        this.$router.push("/");
      } catch (error) {
        this.errors = error.response.data;
      }
    },
  },
};
</script>