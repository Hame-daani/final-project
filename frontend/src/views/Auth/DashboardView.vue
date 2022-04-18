// src/views/Login.vue

<template>
  <v-container>
    <v-card>
      <v-card-title>{{ me.username }}</v-card-title>
      <v-card-text>{{ me.first_name }} {{ me.last_name }}</v-card-text>
      <v-btn @click="logout">logout</v-btn>
    </v-card>
    <v-card>
      <v-card-title>watchlist</v-card-title>
      <v-card-text>{{ watchlist }}</v-card-text>
    </v-card>
    <v-card>
      <v-card-title>favorites</v-card-title>
      <v-card-text>{{ favorites }}</v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return { watchlist: [], favorites: [] };
  },
  computed: { ...mapGetters("auth", { me: "getUser" }) },
  methods: {
    async logout() {
      return this.$store
        .dispatch("auth/logout")
        .then(() => this.$router.push("/"))
        .catch((err) => alert(err.response.data));
    },
  },
};
</script>