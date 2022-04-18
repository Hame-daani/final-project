<template>
  <v-container>
    <v-progress-circular
      indeterminate
      color="red"
      v-if="loading"
    ></v-progress-circular>
    <v-card v-show="!loading">
      <v-card-title>{{ movie.title }}</v-card-title>
      <v-card-subtitle>{{ movie.year }}</v-card-subtitle>
      <v-img aspect-ratio="1.7" :src="movie.poster" contain />
      <v-container>
        <label for="">Average Rating</label>
        <span class="text-caption mr-2">
          ({{ movie.avg_rating | decimalPlace }})
        </span>
        <v-rating
          v-model="movie.avg_rating"
          length="10"
          readonly
          half-increments
        ></v-rating>
      </v-container>
      <v-container v-show="isLoggedIn">
        <label for="">Estimated Rating</label>
        <span class="text-caption mr-2">
          ({{ movie.estimated_rating | decimalPlace }})
        </span>
        <v-rating
          v-model="movie.estimated_rating"
          length="10"
          readonly
          half-increments
        ></v-rating>
      </v-container>
      <v-card-text>{{ movie.plot }}</v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import MoviesService from "@/services/MoviesService";
import { mapGetters } from "vuex";

export default {
  name: "MovieView",
  components: {},
  props: { id: { required: true } },
  data() {
    return { movie: {}, loading: false };
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn"]),
  },
  async created() {
    await this.loadMovie();
  },
  methods: {
    async loadMovie() {
      this.loading = true;
      return MoviesService.getMovie(this.id)
        .then((data) => (this.movie = data))
        .then(() => (this.loading = false))
        .catch((err) => alert(err.response.data));
    },
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