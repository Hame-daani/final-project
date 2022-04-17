<template>
  <v-container>
    <v-progress-circular
      indeterminate
      color="red"
      v-if="loading"
    ></v-progress-circular>
    <v-card v-for="movie in movies" :key="movie.id" :to="`${movie.id}`">
      <v-card-title>{{ movie.title }}</v-card-title>
      <v-card-subtitle>{{ movie.year }}</v-card-subtitle>
    </v-card>
    <v-pagination v-model="page" class="my-4" :length="total_pages">
      ></v-pagination
    >
  </v-container>
</template>

<script>
import MoviesService from "@/services/MoviesService";

export default {
  components: {},
  data() {
    return { loading: false, page: 1, total_pages: 1, movies: [] };
  },
  created() {
    this.loadMovies(this.page);
  },
  methods: {
    async loadMovies() {
      this.loading = true;
      this.movies = [];
      const payload = {
        params: {
          page: this.page,
        },
      };
      return MoviesService.getAll(payload)
        .then((data) => {
          this.movies = data.results;
          this.total_pages = data.total_pages;
        })
        .then(() => {
          this.loading = false;
        })
        .catch((err) => alert(err.response.data));
    },
  },
  watch: {
    page: function () {
      this.loadMovies();
    },
  },
};
</script>

<style>
</style>