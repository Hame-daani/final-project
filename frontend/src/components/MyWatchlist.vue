<template>
  <v-container>
    <v-card>
      <v-card-title> My Watchlist </v-card-title>
      <loading-circular :flag="loading" />
      <movie-preview
        v-for="movie in watchlist"
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
import UsersService from "@/services/UsersService";
import LoadingCircular from "@/components/LoadingCircular.vue";
import MoviePreview from "@/components/MoviePreview.vue";
export default {
  components: {
    LoadingCircular,
    MoviePreview,
  },
  props: {
    id: { required: true },
  },
  async created() {
    return this.loadData();
  },
  data() {
    return {
      watchlist: [],
      page: 1,
      total_pages: 1,
      loading: false,
    };
  },
  methods: {
    async loadData() {
      this.loading = true;
      this.watchlist = [];
      const payload = {
        params: {
          page: this.page,
        },
      };
      return UsersService.getWatchlist(this.id, payload)
        .then((data) => {
          this.watchlist = data.results;
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