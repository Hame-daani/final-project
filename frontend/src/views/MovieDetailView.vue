<template>
  <v-container>
    <v-progress-circular
      indeterminate
      color="red"
      v-if="loading"
    ></v-progress-circular>
    <v-card>
      <v-card-title>{{ movie.title }}</v-card-title>
      <v-card-subtitle>{{ movie.year }}</v-card-subtitle>
      <v-img :src="movie.poster" />
      <v-card-text>{{ movie.plot }}</v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import MoviesService from "@/services/MoviesService";

export default {
  name: "MovieView",
  components: {},
  props: { id: { required: true } },
  data() {
    return { movie: {}, loading: false };
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
};
</script>
