<template>
  <v-container class="">
    <v-container>
      <review-details :id="id" />
    </v-container>
    <v-container>
      <comment-form v-if="isLoggedIn" @comment-submitted="addComment($event)" />
    </v-container>
    <v-container>
      <review-comments :review_id="id" />
    </v-container>
  </v-container>
</template>

<script>
import ReviewDetails from "@/components/ReviewDetails.vue";
import CommentForm from "@/components/CommentForm.vue";
import ReviewsService from "@/services/ReviewsService";
import ReviewComments from "@/components/ReviewComments.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    ReviewDetails,
    CommentForm,
    ReviewComments,
  },
  props: {
    id: { required: true },
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn"]),
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