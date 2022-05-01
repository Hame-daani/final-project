<template>
  <v-container>
    <v-card flat>
      <v-card-title>
        <v-badge color="green" :content="count"> My Reviews </v-badge>
      </v-card-title>
      <loading-circular :flag="loading" />
      <v-divider></v-divider>
      <v-row>
        <v-col v-for="review in reviews" :key="review.id">
          <review-preview :review="review" />
        </v-col>
      </v-row>
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
    id: { required: true },
  },
  async created() {
    return this.loadReviews();
  },
  data() {
    return {
      reviews: [],
      page: 1,
      total_pages: 1,
      count: 0,
      loading: false,
    };
  },
  methods: {
    async loadReviews() {
      this.loading = true;
      this.reviews = [];
      const payload = {
        params: {
          user: this.id,
          page: this.page,
        },
      };
      return ReviewsService.getReviews(payload)
        .then((data) => {
          this.reviews = data.results;
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