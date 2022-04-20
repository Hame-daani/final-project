<template>
  <v-container class="">
    <review-details :id="id" />
    <comment-form @comment-submitted="addComment($event)" />
  </v-container>
</template>

<script>
import ReviewDetails from "@/components/ReviewDetails.vue";
import CommentForm from "@/components/CommentForm.vue";
import ReviewsService from "@/services/ReviewsService";

export default {
  components: {
    ReviewDetails,
    CommentForm,
  },
  props: {
    id: { required: true },
  },
  data() {
    return {};
  },
  methods: {
    async addComment(comment) {
      const payload = {
        text: comment.text,
      };
      return ReviewsService.addComment(this.id, payload)
        .then((data) => console.log(data))
        .catch((err) => console.log(err.response.data));
    },
  },
};
</script>

<style>
</style>