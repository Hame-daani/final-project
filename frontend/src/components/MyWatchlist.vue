<template>
  <v-container>
    <v-card flat :loading="loading">
      <template slot="progress">
        <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
          rounded
        ></v-progress-linear>
      </template>
      <v-card-title>
        <v-badge color="green" :content="count"> My Watchlist </v-badge>
      </v-card-title>
      <v-divider></v-divider>
      <v-row>
        <v-col v-for="movie in watchlist" :key="movie.id">
          <movie-preview :movie="movie" />
        </v-col>
      </v-row>
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
import MoviePreview from "@/components/MoviePreview.vue";
export default {
  components: {
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
      count: 0,
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
          this.count = data.count;
        })
        .then(() => (this.loading = false))
        .catch((err) => console.log(err.reponse.data));
    },
  },
};
</script>

<style>
</style>