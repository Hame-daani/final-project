<template>
  <v-container>
    <v-card>
      <v-card-title> My Reviews </v-card-title>
      <loading-circular :flag="loading" />
      <review-preview
        v-for="review in reviews"
        :key="review.id"
        :review="review"
      />
    </v-card>
    <v-pagination
      v-model="page"
      class="my-4"
      :length="total_pages"
      @input="loadReviews"
    />
  </v-container>
</template>

<script>
import ReviewsService from "@/services/ReviewsService";
import LoadingCircular from "@/components/LoadingCircular.vue";
import ReviewPreview from "@/components/ReviewPreview.vue";

export default {
  components: {
    LoadingCircular,
    ReviewPreview,
  },
  props: {
    user: { required: true },
  },
  async created() {
    console.log("my reviews");
    return this.loadReviews();
  },
  data() {
    return {
      reviews: [],
      page: 1,
      total_pages: 1,
      loading: false,
    };
  },
  methods: {
    async loadReviews() {
      this.loading = true;
      this.reviews = [];
      const payload = {
        params: {
          user: this.user.id,
          page: this.page,
        },
      };
      return ReviewsService.getReviews(payload)
        .then((data) => {
          this.reviews = data.results;
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