<template>
  <v-container>
    <movie-details :id="id" />
    <v-card>
      <v-card-title>My Review</v-card-title>
      <loading-circular :flag="myReviewsLoading" />
      <review-preview v-if="myReview && myReview.id" :review="myReview" />
    </v-card>
  </v-container>
</template>

<script>
import MovieDetails from "@/components/MovieDetails.vue";
import ReviewPreview from "@/components/ReviewPreview.vue";
import { mapGetters } from "vuex";
import ReviewsService from "@/services/ReviewsService";
import LoadingCircular from "@/components/LoadingCircular.vue";

export default {
  props: { id: { required: true } },
  components: {
    MovieDetails,
    ReviewPreview,
    LoadingCircular,
  },
  data() {
    return {
      myReview: {},
      otherReviews: [],
      myReviewsLoading: false,
      otherReviewsLoading: false,
    };
  },
  computed: {
    ...mapGetters("auth", { isLoggedIn: "isLoggedIn", user: "getUser" }),
  },
  created() {
    if (this.isLoggedIn) {
      this.loadMyReview();
    }
    this.loadOtherReviews();
  },
  methods: {
    async loadMyReview() {
      this.myReviewsLoading = true;
      const payload = {
        params: {
          user: this.user.id,
          movie: this.id,
        },
      };
      return ReviewsService.getReviews(payload)
        .then((data) => (this.myReview = data.results[0]))
        .then(() => {
          this.myReviewsLoading = false;
        })
        .catch((err) => alert(err.response.data));
    },
    async loadOtherReviews() {},
  },
};
</script>

<style>
</style>