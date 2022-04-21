<template>
  <v-container>
    <v-card>
      <v-card-title> My Comments </v-card-title>
      <loading-circular :flag="loading" />
      <comments-card
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        @comment-deleted="deleteComment($event)"
      />
    </v-card>
    <v-pagination
      v-model="page"
      class="my-4"
      :length="total_pages"
      @input="loadComments"
    />
  </v-container>
</template>

<script>
import CommentsService from "@/services/CommentsService";
import LoadingCircular from "@/components/LoadingCircular.vue";
import CommentsCard from "@/components/CommentsCard.vue";

export default {
  components: {
    LoadingCircular,
    CommentsCard,
  },
  props: {
    user: { required: true },
  },
  async created() {
    return this.loadComments();
  },
  data() {
    return {
      comments: [],
      page: 1,
      total_pages: 1,
      loading: false,
    };
  },
  methods: {
    async loadComments() {
      this.loading = true;
      this.comments = [];
      const payload = {
        params: {
          user: this.user.id,
          page: this.page,
        },
      };
      return CommentsService.getMyComments(payload)
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