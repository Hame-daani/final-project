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
      const payload = {
        // username: this.username,
        // password: this.password,
        username: "EricWeber4298",
        password: "12345678",
      };
      return this.$store
        .dispatch("auth/login", payload)
        .then(() => this.$router.push("/"))
        .catch((err) => alert(err.response.data.non_field_errors));
    },
  },
};
</script>