
<template>
  <v-container class="d-flex flex-column align-center justify-center">
    <v-card width="500">
      <v-toolbar flat color="blue-grey" dark>
        <v-toolbar-title>Sign Up</v-toolbar-title>
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
        ></v-text-field>
        <v-text-field
          filled
          label="Passwrod (Repeat)"
          v-model="password_repeat"
          type="password"
        ></v-text-field>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error" depressed @click="clear"> Clear </v-btn>
        <v-btn color="success" depressed @click="signUp"> Submit </v-btn>
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
import AuthService from "@/services/AuthService.js";

export default {
  data() {
    return {
      username: "",
      password: "",
      password_repeat: "",
      msg: "",
      alert: false,
      error: "",
    };
  },
  methods: {
    async signUp() {
      const credentials = {
        username: this.username,
        password: this.password,
        password_repeat: this.password_repeat,
        gender: "M",
      };
      if (this.password !== this.password_repeat) {
        this.error = "wrong repeat";
        this.alert = true;
        return;
      }
      return AuthService.signUp(credentials)
        .then(() => {
          this.$router.push({ name: "login" });
        })
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
      this.password_repeat = "";
      this.alret = false;
      this.error = "";
    },
  },
};
</script>