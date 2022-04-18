<template>
  <v-container>
    <v-toolbar dense>
      <v-text-field hide-details single-line v-model="search"></v-text-field>
      <v-btn icon @click="doSearch">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-toolbar>
    <v-select
      v-model="selected_genres"
      :items="genres"
      label="Genres"
      chips
      deletable-chips
      clearable
    ></v-select>
    <v-toolbar dense>
      <v-checkbox v-model="toggle_year"> </v-checkbox>
      <v-slider
        v-model="year"
        label="year"
        thumb-label="always"
        min="1900"
        max="2022"
        :disabled="!toggle_year"
      ></v-slider>
    </v-toolbar>
    <loading-circular :flag="loading" />
    <movie-preview v-for="movie in movies" :movie="movie" :key="movie.id" />
    <v-pagination
      v-model="page"
      class="my-4"
      :length="total_pages"
      @input="loadMovies"
    />
  </v-container>
</template>

<script>
import MoviesService from "@/services/MoviesService";
import MoviePreview from "@/components/MoviePreview.vue";
import LoadingCircular from "@/components/LoadingCircular.vue";

export default {
  components: { MoviePreview, LoadingCircular },
  data() {
    return {
      loading: false,
      toggle_year: false,
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
    doSearch() {
      this.page = 1;
      return this.loadMovies();
    },
    async loadMovies() {
      this.loading = true;
      this.movies = [];
      const payload = {
        params: {
          page: this.page,
          genres: this.selected_genres,
          year: this.toggle_year ? this.year : "",
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
};
</script>

<style>
</style>