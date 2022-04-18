<template>
  <v-card :to="`reviews/${me.id}`">
    <v-card-title>{{ me.movie.title }}</v-card-title>
    <v-card-subtitle>{{ me.created_at }}</v-card-subtitle>
    <v-card-subtitle>{{ me.user.username }}</v-card-subtitle>
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
  },
  data() {
    return { me: this.review };
  },
};
</script>

<style>
</style>