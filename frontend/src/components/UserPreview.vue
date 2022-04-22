<template>
  <v-card :to="{ name: 'profile', params: { id: me.id } }">
    <v-card-title>{{ me.username }}</v-card-title>
    <v-card-subtitle>{{ me.similarity }}</v-card-subtitle>
    <v-card-text> {{ me.first_name }} {{ me.last_name }} </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    user: { required: true },
  },
  data() {
    return { me: this.user };
  },
};
</script>

<style>
</style>