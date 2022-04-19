<template>
  <v-container>
    <v-card v-if="!editing">
      <v-card-title> {{ user.username }} </v-card-title>
      <v-card-text>
        Name: {{ user.first_name }} {{ user.last_name }}
      </v-card-text>
      <v-card-text> Email: {{ user.email }} </v-card-text>
      <v-card-text> Gender: {{ user.gender }} </v-card-text>
      <v-btn color="info" @click="enableEditing">Edit</v-btn>
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
  </v-container>
</template>

<script>
import UsersService from "@/services/UsersService";

export default {
  props: {
    user: { required: true },
  },
  created() {
    this.signal();
  },
  data() {
    return {
      me: {
        id: this.user.id,
        first_name: this.user.first_name,
        last_name: this.user.last_name,
        email: this.user.email,
      },
      editing: false,
    };
  },
  methods: {
    signal() {
      console.log("my profile");
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