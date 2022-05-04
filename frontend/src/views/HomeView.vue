<template>
  <v-container>
    <v-card class="my-50">
      <v-expansion-panels accordion v-model="panelIndex" v-if="isLoggedIn">
        <v-expansion-panel>
          <v-expansion-panel-header>
            Global Recommendations
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-card class="my-50" :loading="globalLoading">
              <v-toolbar flat color="blue-grey" dark>
                <v-toolbar-title>Global Recommendation</v-toolbar-title>
              </v-toolbar>
              <template slot="progress">
                <v-progress-linear
                  color="deep-purple"
                  height="10"
                  indeterminate
                  rounded
                ></v-progress-linear>
              </template>
              <v-slide-group show-arrows>
                <v-slide-item v-for="movie in globalRecs" :key="movie.id">
                  <movie-preview :movie="movie" />
                </v-slide-item>
              </v-slide-group>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>
            Friends Recommendations
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-card class="my-50" :loading="friendsLoading">
              <v-toolbar flat color="blue-grey" dark>
                <v-toolbar-title>Friends Recommendation</v-toolbar-title>
              </v-toolbar>
              <template slot="progress">
                <v-progress-linear
                  color="deep-purple"
                  height="10"
                  indeterminate
                  rounded
                ></v-progress-linear>
              </template>
              <v-slide-group show-arrows>
                <v-slide-item v-for="movie in friendsRecs" :key="movie.id">
                  <movie-preview :movie="movie" />
                </v-slide-item>
              </v-slide-group>
            </v-card>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>

    <v-card class="ma-10" :loading="recentReviewsLoading">
      <v-toolbar flat color="blue-grey" dark>
        <v-toolbar-title>Recent Reviews</v-toolbar-title>
      </v-toolbar>
      <template slot="progress">
        <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
          rounded
        ></v-progress-linear>
      </template>
      <v-slide-group show-arrows>
        <v-slide-item
          class="me-3"
          v-for="review in recentReviews"
          :key="review.id"
        >
          <review-preview :review="review" />
        </v-slide-item>
      </v-slide-group>
    </v-card>

    <template v-if="isLoggedIn">
      <v-card class="ma-10" :loading="friendsReviewsLoading">
        <v-toolbar flat color="blue-grey" dark>
          <v-toolbar-title>Friends Reviews</v-toolbar-title>
        </v-toolbar>
        <template slot="progress">
          <v-progress-linear
            color="deep-purple"
            height="10"
            indeterminate
            rounded
          ></v-progress-linear>
        </template>
        <v-slide-group show-arrows>
          <v-slide-item
            class="me-3"
            v-for="review in friendsRecentReviews"
            :key="review.id"
          >
            <review-preview :review="review" />
          </v-slide-item>
        </v-slide-group>
      </v-card>
    </template>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import ReviewPreview from "@/components/ReviewPreview.vue";
import MoviePreview from "@/components/MoviePreview.vue";
import ReviewsService from "@/services/ReviewsService";
import RecommenderService from "@/services/RecommenderService";

export default {
  components: {
    ReviewPreview,
    MoviePreview,
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
      slide: null,
      panelIndex: -1,
    };
  },
  async created() {
    this.loadRecentReviews();
    if (this.isLoggedIn) {
      this.loadFriendsReviews();
      // await this.loadGlobalRecs();
      // await this.loadFriendsRecs();
    }
  },
  watch: {
    panelIndex: function () {
      if (this.panelIndex === 0) {
        this.loadGlobalRecs();
      }
      if (this.panelIndex === 1) {
        this.loadFriendsRecs();
      }
    },
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