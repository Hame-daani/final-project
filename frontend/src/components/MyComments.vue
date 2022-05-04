<template>
  <v-container>
    <v-card flat :loading="loading">
      <template slot="progress">
        <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
          rounded
        ></v-progress-linear>
      </template>
      <v-card-title>
        <v-badge color="green" :content="count"> My Comments </v-badge>
      </v-card-title>
      <v-divider></v-divider>
      <comment-card
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :preview="true"
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
import CommentCard from "@/components/CommentCard.vue";

export default {
  components: {
    CommentCard,
  },
  props: {
    id: { required: true },
  },
  async created() {
    return this.loadComments();
  },
  data() {
    return {
      comments: [],
      page: 1,
      total_pages: 1,
      count: 0,
      loading: false,
    };
  },
  methods: {
    async loadComments() {
      this.loading = true;
      this.comments = [];
      const payload = {
        params: {
          user: this.id,
          page: this.page,
        },
      };
      return CommentsService.getMyComments(payload)
        .then((data) => {
          this.comments = data.results;
          this.total_pages = data.total_pages;
          this.count = data.count;
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