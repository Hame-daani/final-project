<template>
  <v-card v-show="isLoggedIn">
    <v-card-title>Friends Recommendation</v-card-title>
    <v-progress-circular
      indeterminate
      color="red"
      v-if="loading"
    ></v-progress-circular>
    <v-card v-for="movie in movies" :key="movie.id" :to="`movies/${movie.id}`">
      <v-card-title>{{ movie.title }}</v-card-title>
      <v-card-subtitle>{{ movie.estimated_rating }}</v-card-subtitle>
    </v-card>
  </v-card>
</template>

<script>
import RecommenderService from "@/services/RecommenderService";
import { mapGetters } from "vuex";

export default {
  data() {
    return { loading: false, movies: [] };
  },
  computed: {
    ...mapGetters("auth", { isLoggedIn: "isLoggedIn" }),
  },
  created() {
    if (this.isLoggedIn) {
      this.loadMovies();
    }
  },
  methods: {
    async loadMovies() {
      this.loading = true;
      this.movies = [];
      return RecommenderService.getFriendsRecommendation()
        .then((data) => {
          this.movies = data.results;
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