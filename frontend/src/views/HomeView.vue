<template>
  <v-container>
    <v-card>
      <v-toolbar flat color="blue-grey" dark>
        <v-toolbar-title>Recent Reviews</v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <loading-circular :flag="recentReviewsLoading" />
        <v-row class="justify-space-around">
          <v-col v-for="review in recentReviews" :key="review.id" cols="5">
            <review-preview :review="review" />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-container v-show="isLoggedIn">
      <v-card>
        <v-toolbar flat color="blue-grey" dark>
          <v-toolbar-title>Friends Reviews</v-toolbar-title>
        </v-toolbar>
        <loading-circular :flag="friendsReviewsLoading" />
        <v-row class="justify-space-around">
          <v-col
            v-for="review in friendsRecentReviews"
            :key="review.id"
            cols="5"
          >
            <review-preview :review="review" />
          </v-col>
        </v-row>
      </v-card>
      <v-card>
        <v-toolbar flat color="blue-grey" dark>
          <v-toolbar-title>Global Recomendation</v-toolbar-title>
        </v-toolbar>
        <loading-circular :flag="globalLoading" />
        <v-row class="justify-space-around">
          <v-col v-for="movie in globalRecs" :key="movie.id" cols="5">
            <movie-preview :movie="movie" />
          </v-col>
        </v-row>
      </v-card>
      <v-card>
        <v-toolbar flat color="blue-grey" dark>
          <v-toolbar-title>Friends Recommendation</v-toolbar-title>
        </v-toolbar>
        <loading-circular :flag="friendsLoading" />
        <v-row class="justify-space-around">
          <v-col v-for="movie in friendsRecs" :key="movie.id" cols="5">
            <movie-preview :movie="movie" />
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import ReviewPreview from "@/components/ReviewPreview.vue";
import LoadingCircular from "@/components/LoadingCircular.vue";
import MoviePreview from "@/components/MoviePreview.vue";
import ReviewsService from "@/services/ReviewsService";
import RecommenderService from "@/services/RecommenderService";

export default {
  components: {
    ReviewPreview,
    MoviePreview,
    LoadingCircular,
  },
  data() {
    return {
      recentReviewsLoading: false,
      friendsReviewsLoading: false,
      globalLoading: false,
      friendsLoading: false,
      recentReviews: [],
      friendsRecentReviews: [],
      globalRecs: [],
      friendsRecs: [],
    };
  },
  async created() {
    await this.loadRecentReviews();
    if (this.isLoggedIn) {
      await this.loadFriendsReviews();
      await this.loadGlobalRecs();
      await this.loadFriendsRecs();
    }
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn"]),
  },
  methods: {
    async loadRecentReviews() {
      this.recentReviewsLoading = true;
      this.recentReviews = [];
      return ReviewsService.getRecent()
        .then((data) => {
          this.recentReviews = data;
        })
        .then(() => {
          this.recentReviewsLoading = false;
        })
        .catch((err) => alert(err.response.data));
    },
    async loadFriendsReviews() {
      this.friendsReviewsLoading = true;
      this.friendsRecentReviews = [];
      return ReviewsService.getFriendsRecent()
        .then((data) => {
          this.friendsRecentReviews = data;
        })
        .then(() => {
          this.friendsReviewsLoading = false;
        })
        .catch((err) => alert(err.response.data));
    },
    async loadGlobalRecs() {
      this.globalLoading = true;
      this.globalRecs = [];
      return RecommenderService.getGlobalRecommendation()
        .then((data) => {
          this.globalRecs = data.results;
        })
        .then(() => {
          this.globalLoading = false;
        })
        .catch((err) => alert(err.response.data));
    },
    async loadFriendsRecs() {
      this.friendsLoading = true;
      this.friendsRecs = [];
      return RecommenderService.getFriendsRecommendation()
        .then((data) => {
          this.friendsRecs = data.results;
        })
        .then(() => {
          this.friendsLoading = false;
        })
        .catch((err) => alert(err.response.data));
    },
  },
};
</script>

<style>
</style>