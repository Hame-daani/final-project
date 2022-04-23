<template>
  <v-container>
    <v-card>
      <v-card-title>Recent Reviews</v-card-title>
      <loading-circular :flag="recentReviewsLoading" />
      <review-preview
        v-for="review in recentReviews"
        :review="review"
        :key="review.id"
      />
    </v-card>
    <v-container v-show="isLoggedIn">
      <v-card>
        <v-card-title>Friends Reviews</v-card-title>
        <loading-circular :flag="friendsReviewsLoading" />
        <review-preview
          v-for="review in friendsRecentReviews"
          :review="review"
          :key="review.id"
        />
      </v-card>
      <v-card>
        <v-card-title>GLobal Recommendations</v-card-title>
        <loading-circular :flag="globalLoading" />
        <movie-preview
          v-for="movie in globalRecs"
          :movie="movie"
          :key="movie.id"
        />
      </v-card>
      <v-card>
        <v-card-title>Friends Recommendations</v-card-title>
        <loading-circular :flag="friendsLoading" />
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