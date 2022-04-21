<template>
  <v-container>
    <v-tabs v-model="tab">
      <v-tab v-for="item in items" :key="item.tab">
        {{ item.tab }}
      </v-tab>
    </v-tabs>
    <v-card flat>
      <v-card-text>
        <component
          v-bind:is="items[tab].content"
          :key="tab"
          :user="me"
        ></component>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import MyComments from "@/components/MyComments.vue";
import MyProfile from "@/components/MyProfile.vue";
import MyReqs from "@/components/MyReqs.vue";
import MyReviews from "@/components/MyReviews.vue";
import TasteGroup from "@/components/TasteGroup.vue";
import MyWatchlist from "@/components/MyWatchlist.vue";
import MyFavorites from "@/components/MyFavorites.vue";

export default {
  components: {
    MyComments,
    MyProfile,
    MyReqs,
    MyReviews,
    TasteGroup,
    MyWatchlist,
    MyFavorites,
  },
  data() {
    return {
      tab: 0,
      items: [
        { tab: "Profile", content: MyProfile },
        { tab: "Comments", content: MyComments },
        { tab: "Reviews", content: MyReviews },
        { tab: "Watchlist", content: MyWatchlist },
        { tab: "Favorites", content: MyFavorites },
        { tab: "Friends Requests", content: MyReqs },
        { tab: "Taste Group", content: TasteGroup },
      ],
    };
  },
  computed: { ...mapGetters("auth", { me: "getUser" }) },
  methods: {
    async logout() {
      return this.$store
        .dispatch("auth/logout")
        .then(() => this.$router.push({ name: "login" }))
        .catch((err) => alert(err.response.data));
    },
  },
};
</script>