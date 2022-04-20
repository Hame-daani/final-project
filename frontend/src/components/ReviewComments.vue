<template>
  <v-card>
    <v-container>
      <comment-form v-if="isLoggedIn" @comment-submitted="addComment($event)" />
    </v-container>
    <v-card-title> Comments </v-card-title>
    <v-card :loading="loading">
      <v-card-text>
        <comment-card
          v-for="comment in comments"
          :key="comment.id"
          :comment="comment"
          @comment-deleted="deleteComment($event)"
        />
      </v-card-text>
      <v-pagination
        v-model="page"
        class="my-4"
        :length="total_pages"
        @input="loadComments"
      />
    </v-card>
  </v-card>
</template>

<script>
import ReviewsService from "@/services/ReviewsService";
import CommentCard from "@/components/CommentsCard.vue";
import CommentForm from "@/components/CommentForm.vue";
import { mapGetters } from "vuex";
export default {
  components: {
    CommentCard,
    CommentForm,
  },
  props: {
    review_id: { required: true },
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn", "getUser"]),
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
    async addComment(text) {
      const payload = {
        text: text,
      };
      return ReviewsService.addComment(this.review_id, payload)
        .then((data) => this.comments.push(data))
        .catch((err) => console.log(err.response.data));
    },
    async loadComments() {
      this.comments = [];
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
    deleteComment(id) {
      this.comments = this.comments.filter((obj) => obj.id !== id);
    },
  },
};
</script>

<style>
</style>