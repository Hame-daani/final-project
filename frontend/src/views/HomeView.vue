<template>
  <v-container>
    <recent-reviews />
    <v-divider />
    <recent-friends-reviews />
  </v-container>
</template>

<script>
import RecentReviews from "@/components/RecentReviews.vue";
import RecentFriendsReviews from "@/components/RecentFriendsReviews.vue";

export default {
  components: {
    RecentReviews,
    RecentFriendsReviews,
  },
};
</script>

<style>
</style>