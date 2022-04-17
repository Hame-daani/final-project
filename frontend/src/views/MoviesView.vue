<template>
  <v-container>
    <v-toolbar dense>
      <v-text-field hide-details single-line v-model="search"></v-text-field>
      <v-btn icon @click="loadMovies">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-toolbar>
    <v-combobox
      v-model="selected_genres"
      :items="genres"
      label="Genres"
      multiple
      chips
      deletable-chips
      clearable
    ></v-combobox>
    <v-slider
      v-model="year"
      label="year"
      thumb-label="always"
      min="1900"
      max="2022"
    ></v-slider>
    <v-progress-circular
      indeterminate
      color="red"
      v-if="loading"
    ></v-progress-circular>
    <v-card v-for="movie in movies" :key="movie.id" :to="`${movie.id}`">
      <v-card-title>{{ movie.title }}</v-card-title>
      <v-card-subtitle>{{ movie.year }}</v-card-subtitle>
      <v-card-text>{{ movie.genres }}</v-card-text>
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
      year: "",
      selected_genres: [],
      genres: [
        "Adventure",
        "Animation",
        "Children",
        "Comedy",
        "Fantasy",
        "Romance",
        "Drama",
        "Action",
        "Crime",
        "Thriller",
        "Horror",
        "Mystery",
        "Sci-Fi",
        "IMAX",
        "Documentar",
        "War",
        "Musical",
        "Western",
        "Film-Noir",
      ],
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
          genres: this.selected_genres,
          year: this.year,
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