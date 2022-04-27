<template>
  <v-containter>
    <v-card max-width="500">
      <v-toolbar flat color="blue-grey" dark>
        <v-toolbar-title>Login</v-toolbar-title>
      </v-toolbar>

      <v-card-text>
        <v-text-field filled label="Username" :value="username"></v-text-field>
        <v-text-field filled label="Passwrod" :value="password"></v-text-field>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" depressed> Clear </v-btn>
        <v-btn color="success" depressed @click="login"> Login </v-btn>
      </v-card-actions>
    </v-card>
  </v-containter>
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
        .then(() => this.$router.push({ name: "dashboard" }))
        .catch((err) => alert(err.response.data.non_field_errors));
    },
  },
};
</script>