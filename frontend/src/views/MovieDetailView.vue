<template>
  <v-container>
    <movie-details :id="id" />
  </v-container>
</template>

<script>
import MovieDetails from "@/components/MovieDetails.vue";
export default {
  props: { id: { required: true } },
  components: {
    MovieDetails,
  },
};
</script>

<style>
</style>