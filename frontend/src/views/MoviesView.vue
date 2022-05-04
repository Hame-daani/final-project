<template>
  <v-container>
    <v-card class="ma-5" shaped>
      <!-- search -->
      <v-toolbar flat color="blue-grey" dark>Search</v-toolbar>
      <v-row>
        <v-col class="ma-3" cols="8">
          <v-text-field
            label="Type movie title here..."
            hide-details
            single-line
            clearable
            @keyup.enter="doSearch"
            v-model="search"
          ></v-text-field>
          <v-row>
            <v-col>
              <v-select
                v-model="selected_genres"
                :items="genres"
                label="Genres"
                chips
                deletable-chips
                clearable
              ></v-select>
            </v-col>
            <v-col class="d-flex align-center">
              <v-checkbox v-model="toggle_year"> </v-checkbox>
              <v-slider
                class="mt-5"
                v-model="year"
                label="year"
                thumb-label="always"
                min="1900"
                max="2022"
                :disabled="!toggle_year"
              ></v-slider>
            </v-col>
          </v-row>
        </v-col>
        <v-col class="d-flex justify-center align-center">
          <v-btn @click="doSearch" rounded>
            Search
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card class="ma-5 mt-10" :loading="loading" shaped>
      <!-- result  -->
      <v-toolbar flat color="blue-grey" dark>
        Results <span v-if="count">: Total of ({{ count }})</span></v-toolbar
      >
      <template slot="progress">
        <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
          rounded
        ></v-progress-linear>
      </template>
      <v-row class="mt-3">
        <v-col v-for="movie in movies" :key="movie.id">
          <movie-preview :movie="movie" />
        </v-col>
      </v-row>
      <v-pagination
        v-model="page"
        class="my-4"
        :length="total_pages"
        @input="loadMovies"
        total-visible="10"
      />
    </v-card>
  </v-container>
</template>

<script>
import MoviesService from "@/services/MoviesService";
import MoviePreview from "@/components/MoviePreview.vue";

export default {
  components: { MoviePreview },
  data() {
    return {
      loading: false,
      toggle_year: false,
      movies: [],
      page: 1,
      total_pages: 1,
      count: 0,
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
          search: this.search,
        },
      };
      return MoviesService.getAll(payload)
        .then((data) => {
          this.movies = data.results;
          this.total_pages = data.total_pages;
          this.count = data.count;
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