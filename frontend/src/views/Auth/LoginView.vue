<template>
  <v-container class="d-flex flex-column align-center justify-center">
    <v-card width="500">
      <v-toolbar flat color="blue-grey" dark>
        <v-toolbar-title>Login</v-toolbar-title>
      </v-toolbar>

      <v-card-text>
        <v-text-field
          filled
          label="Username"
          v-model="username"
          type="username"
        ></v-text-field>
        <v-text-field
          filled
          label="Passwrod"
          v-model="password"
          type="password"
          @keyup.enter="login"
        ></v-text-field>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" depressed @click="clear"> Clear </v-btn>
        <v-btn color="success" depressed @click="login"> Login </v-btn>
      </v-card-actions>
    </v-card>
    <v-alert
      v-model="alert"
      class="mt-5"
      prominent
      type="error"
      width="500"
      dismissible
    >
      {{ error }}
    </v-alert>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      alert: false,
      error: "",
    };
  },
  methods: {
    async login() {
      const payload = {
        username: this.username,
        password: this.password,
        // username: "EricWeber4298",
        // password: "12345678",
      };
      return this.$store
        .dispatch("auth/login", payload)
        .then(() => this.$router.push({ name: "dashboard" }))
        .catch((err) => {
          this.error = "";
          for (const [key, value] of Object.entries(err.response.data))
            this.error += `${key}: ${value} \n`;
          this.alert = true;
        });
    },
    clear() {
      this.username = "";
      this.password = "";
    },
  },
};
</script>