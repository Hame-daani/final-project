<template>
  <v-container>
    <v-card>
      <v-card-title> My Favorites </v-card-title>
      <loading-circular :flag="loading" />
      <movie-preview
        v-for="movie in favorites"
        :key="movie.id"
        :movie="movie"
      />
    </v-card>
    <v-pagination
      v-model="page"
      class="my-4"
      :length="total_pages"
      @input="loadData"
    />
  </v-container>
</template>

<script>
import LoadingCircular from "@/components/LoadingCircular.vue";
import MoviePreview from "@/components/MoviePreview.vue";
import UsersService from "@/services/UsersService";

export default {
  components: {
    LoadingCircular,
    MoviePreview,
  },
  props: {
    user: { required: true },
  },
  async created() {
    return this.loadData();
  },
  data() {
    return {
      favorites: [],
      page: 1,
      total_pages: 1,
      loading: false,
    };
  },
  methods: {
    async loadData() {
      this.loading = true;
      this.favorites = [];
      const payload = {
        params: {
          page: this.page,
        },
      };
      return UsersService.getFavorites(this.user.id, payload)
        .then((data) => {
          this.favorites = data.results;
          this.total_pages = data.total_pages;
        })
        .then(() => (this.loading = false))
        .catch((err) => console.log(err.reponse.data));
    },
  },
};
</script>

<style>
</style>