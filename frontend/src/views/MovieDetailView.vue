<template>
  <v-container>
    <v-container>
      <movie-details :id="id" :reviewCounts="reviewCounts" />
    </v-container>
    <v-container>
      <v-card shaped>
        <v-card-title>Similar Movies</v-card-title>
        <loading-circular :flag="similarMoviesLoading" />
        <v-slide-group v-model="slide" show-arrows>
          <v-slide-item
            class="me-3"
            v-for="movie in similarMovies"
            :key="movie.id"
          >
            <movie-preview :key="movie.id" :movie="movie" />
          </v-slide-item>
        </v-slide-group>
      </v-card>
    </v-container>
    <v-container v-if="isLoggedIn">
      <v-card shaped>
        <v-card-title>My Review</v-card-title>
        <loading-circular :flag="myReviewsLoading" />
        <v-container>
          <review-preview
            v-if="!myReviewsLoading && myReview"
            :review="myReview"
            :showMovie="false"
          />
          <review-form
            v-if="!myReviewsLoading && !myReview"
            @review-submited="submitReview($event)"
          />
        </v-container>
      </v-card>
    </v-container>
    <v-container>
      <v-card>
        <v-card-title>Others Reviews</v-card-title>
        <loading-circular :flag="otherReviewsLoading" />
        <v-row>
          <review-preview
            v-for="review in otherReviews"
            :key="review.id"
            :review="review"
            :showMovie="false"
          />
        </v-row>
        <v-pagination
          v-model="reviewsPage"
          class="my-10"
          :length="reviews_total_pages"
          @input="loadOtherReviews"
          :total-visible="10"
        />
      </v-card>
    </v-container>
  </v-container>
</template>

<script>
import MovieDetails from "@/components/MovieDetails.vue";
import ReviewPreview from "@/components/ReviewPreview.vue";
import { mapGetters } from "vuex";
import ReviewsService from "@/services/ReviewsService";
import LoadingCircular from "@/components/LoadingCircular.vue";
import RecommenderService from "@/services/RecommenderService";
import MoviePreview from "@/components/MoviePreview.vue";
import ReviewForm from "@/components/ReviewForm.vue";

export default {
  props: { id: { required: true } },
  components: {
    MovieDetails,
    ReviewPreview,
    LoadingCircular,
    MoviePreview,
    ReviewForm,
  },
  data() {
    return {
      myReview: {},
      otherReviews: [],
      similarMovies: [],
      reviewCounts: 0,
      reviewsPage: 1,
      reviews_total_pages: 1,
      myReviewsLoading: false,
      otherReviewsLoading: false,
      similarMoviesLoading: false,
    };
  },
  computed: {
    ...mapGetters("auth", { isLoggedIn: "isLoggedIn", user: "getUser" }),
  },
  async created() {
    if (this.isLoggedIn) {
      await this.loadMyReview();
    }
    await this.loadSimilarMovies();
    await this.loadOtherReviews();
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
    async loadOtherReviews() {
      this.otherReviewsLoading = true;
      this.otherReviews = [];
      const payload = {
        params: {
          movie: this.id,
          page: this.reviewsPage,
        },
      };
      return ReviewsService.getReviews(payload)
        .then((data) => {
          this.otherReviews = data.results;
          this.reviews_total_pages = data.total_pages;
          this.reviewCounts = data.count;
        })
        .then(() => {
          this.otherReviewsLoading = false;
        })
        .catch((err) => alert(err.response.data));
    },
    async loadSimilarMovies() {
      this.similarMoviesLoading = true;
      return RecommenderService.getSimilarMovies(this.id)
        .then((data) => (this.similarMovies = data.results))
        .then(() => (this.similarMoviesLoading = false))
        .catch((err) => alert(err.response.data));
    },
    async submitReview(review) {
      const payload = {
        movie: this.id,
        text: review.text,
        rating: Number(review.rating),
      };
      return ReviewsService.create(payload)
        .then((data) => (this.myReview = data))
        .catch((err) => {
          console.log(err.response.data);
        });
    },
  },
};
</script>

<style>
</style>