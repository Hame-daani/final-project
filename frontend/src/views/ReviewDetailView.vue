<template>
  <v-container class="">
    <v-row>
      <v-col>
        <review-details :id="id" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ReviewDetails from "@/components/ReviewDetails.vue";

export default {
  components: {
    ReviewDetails,
  },
  props: {
    id: { required: true },
  },
  data() {
    return {};
  },
};
</script>

<style>
</style>