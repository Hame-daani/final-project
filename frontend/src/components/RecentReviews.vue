<template>
  <v-card>
    <v-card-title>Recent Reviews</v-card-title>
    <v-progress-circular
      indeterminate
      color="red"
      v-if="loading"
    ></v-progress-circular>
    <v-card
      v-for="review in reviews"
      :key="review.id"
      :to="`reviews/${review.id}`"
    >
      <v-card-title>{{ review.movie.title }}</v-card-title>
      <v-card-subtitle>{{ review.created_at }}</v-card-subtitle>

      <v-card-text>
        {{ review.user.username }}
      </v-card-text>
    </v-card>
  </v-card>
</template>

<script>
import ReviewsService from "@/services/ReviewsService";

export default {
  data() {
    return { loading: false, reviews: [] };
  },
  created() {
    this.loadReviews();
  },
  methods: {
    async loadReviews() {
      this.loading = true;
      this.reviews = [];
      return ReviewsService.getRecent()
        .then((data) => {
          this.reviews = data;
        })
        .then(() => {
          this.loading = false;
        })
        .catch((err) => alert(err.response.data));
    },
  },
};
</script>

<style>
</style>