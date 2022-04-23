<template>
  <v-container class="">
    <v-container>
      <review-details :id="id" />
    </v-container>
    <v-container>
      <review-comments :review_id="id" />
    </v-container>
  </v-container>
</template>

<script>
import ReviewDetails from "@/components/ReviewDetails.vue";
import ReviewComments from "@/components/ReviewComments.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    ReviewDetails,
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
  methods: {},
};
</script>

<style>
</style>