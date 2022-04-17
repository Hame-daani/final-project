<template>
  <v-container>
    <v-toolbar dense>
      <v-text-field hide-details single-line v-model="search"></v-text-field>
    </v-toolbar>

    <v-btn icon @click="loadMovies">
      <v-icon>mdi-magnify</v-icon>
    </v-btn>
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
    return {
      loading: false,
      movies: [],
      page: 1,
      total_pages: 1,
      search: "",
      genres: [],
      year: "",
    };
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
          search: encodeURIComponent(this.search.trim()),
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