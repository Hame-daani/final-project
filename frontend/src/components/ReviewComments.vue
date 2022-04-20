<template>
  <v-card :loading="loading">
    <v-card-title> Comments </v-card-title>
    <v-card-text>
      <comment-card
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
      />
    </v-card-text>
    <v-pagination
      v-model="page"
      class="my-4"
      :length="total_pages"
      @input="loadComments"
    />
  </v-card>
</template>

<script>
import ReviewsService from "@/services/ReviewsService";
import CommentCard from "@/components/CommentsCard.vue";

export default {
  components: {
    CommentCard,
  },
  props: {
    review_id: { required: true },
  },
  data() {
    return {
      comments: [],
      page: 1,
      total_pages: 1,
      loading: false,
    };
  },
  async created() {
    return this.loadComments();
  },
  methods: {
    async loadComments() {
      this.loading = true;
      const payload = {
        params: {
          page: this.page,
        },
      };
      return ReviewsService.getComments(this.review_id, payload)
        .then((data) => {
          this.comments = data.results;
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