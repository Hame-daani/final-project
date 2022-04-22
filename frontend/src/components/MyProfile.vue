<template>
  <v-card v-if="!editing">
    <v-card-title> {{ me.username }} </v-card-title>
    <v-card-text> Name: {{ me.first_name }} {{ me.last_name }} </v-card-text>
    <v-card-text> Email: {{ me.email }} </v-card-text>
    <v-card-text> Gender: {{ me.gender }} </v-card-text>
    <v-card-actions v-if="isLoggedIn">
      <v-btn v-if="getUser.id === this.id" color="info" @click="enableEditing"
        >Edit</v-btn
      >
      <v-btn v-if="isFriend" color="info">UnFollow</v-btn>
      <v-btn v-if="!isFriend" color="info">Follow</v-btn>
    </v-card-actions>
  </v-card>
  <v-card v-else>
    <v-card-title> Editing Your Info </v-card-title>
    <template>
      <v-form ref="form">
        <v-text-field
          label="First Name"
          v-model="me.first_name"
          hide-details="auto"
          required
        ></v-text-field>
        <v-text-field
          label="Last Name"
          v-model="me.last_name"
          hide-details="auto"
          required
        ></v-text-field>
        <v-text-field
          label="Email"
          v-model="me.email"
          hide-details="auto"
          required
        ></v-text-field>
        <v-btn @click="update" color="info"> Update </v-btn>
        <v-btn @click="cancel" color="yellow"> Cancel </v-btn>
      </v-form>
    </template>
  </v-card>
</template>

<script>
import UsersService from "@/services/UsersService";
import { mapGetters } from "vuex";

export default {
  props: {
    id: { required: true },
  },
  computed: { ...mapGetters("auth", ["isLoggedIn", "getUser"]) },
  data() {
    return {
      me: {},
      editing: false,
      isFriend: false,
    };
  },
  async created() {
    if (!this.id || this.id === this.getUser.id) this.me = this.getUser;
    else await this.loadData();
    if (this.isLoggedIn && this.id !== this.getUser.id) this.loadFriendship();
  },
  methods: {
    async loadData() {
      return UsersService.getUser(this.id)
        .then((data) => (this.me = data))
        .catch((err) => console.log(err.reponse.data));
    },
    async loadFriendship() {
      return UsersService.getFriendship(this.me.id)
        .then((data) => {
          this.isFriend = data.isFriend;
        })
        .catch((err) => console.log(err.reponse.data));
    },
    enableEditing() {
      this.editing = true;
    },
    async update() {
      return UsersService.update(this.me)
        .then((result) => {
          this.$store.commit("auth/SET_USER", result);
        })
        .then(() => (this.editing = false))
        .catch((err) => {
          console.log(err.response.data);
        });
    },
    cancel() {
      this.editing = false;
    },
  },
};
</script>

<style>
</style>