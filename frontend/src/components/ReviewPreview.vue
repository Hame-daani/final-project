<template>
  <v-card :to="{ name: 'review', params: { id: me.id } }">
    <template v-if="showMovie">
      <v-card-title>{{ me.movie.title }}</v-card-title>
      <v-card-subtitle>{{ me.user.username }}</v-card-subtitle>
    </template>
    <template v-else>
      <v-card-title>{{ me.user.username }}</v-card-title>
    </template>
    <v-card-subtitle>{{ me.created_at }}</v-card-subtitle>
    <v-rating v-model="me.rating" length="10" readonly></v-rating>
    <v-card-text>
      {{ me.text }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    review: { required: true },
    showMovie: { type: Boolean, default: true },
  },
  data() {
    return { me: this.review };
  },
};
</script>

<style>
</style>