<template>
  <v-card :to="{ name: 'movie', params: { id: me.id } }">
    <v-card-title>{{ me.title }}</v-card-title>
    <v-card-subtitle>{{ me.year }}</v-card-subtitle>
    <v-container>
      <label for="">Average Rating</label>
      <span class="text-caption mr-2">
        ({{ me.avg_rating | decimalPlace }})
      </span>
      <v-rating
        v-model="me.avg_rating"
        length="10"
        readonly
        half-increments
      ></v-rating>
    </v-container>
    <v-container v-show="me.estimated_rating">
      <label for="">Estimated Rating</label>
      <span class="text-caption mr-2">
        ({{ me.estimated_rating | decimalPlace }})
      </span>
      <v-rating
        v-model="me.estimated_rating"
        length="10"
        readonly
        half-increments
      ></v-rating>
    </v-container>
    <v-card-text>{{ me.genres }}</v-card-text>
  </v-card>
</template>

<script>
export default {
  props: { movie: { required: true } },
  data() {
    return {
      me: this.movie,
    };
  },
  filters: {
    decimalPlace(num) {
      return parseFloat(num).toFixed(2);
    },
  },
};
</script>

<style>
</style>