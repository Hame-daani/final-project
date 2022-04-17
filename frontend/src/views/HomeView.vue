<template>
  <v-container>
    <recent-reviews />
    <v-divider />
    <recent-friends-reviews />
    <v-divider />
    <global-rec />
    <v-divider />
    <friends-rec />
  </v-container>
</template>

<script>
import RecentReviews from "@/components/RecentReviews.vue";
import RecentFriendsReviews from "@/components/RecentFriendsReviews.vue";
import GlobalRec from "@/components/GlobalRec.vue";
import FriendsRec from "@/components/FriendsRec.vue";

export default {
  components: {
    RecentReviews,
    RecentFriendsReviews,
    GlobalRec,
    FriendsRec,
  },
};
</script>

<style>
</style>