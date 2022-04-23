<template>
  <v-container>
    <v-tabs v-model="tab" center-active>
      <v-tab v-for="item in items" :key="item.tab">
        {{ item.tab }}
      </v-tab>
    </v-tabs>
    <v-card flat>
      <v-card-text>
        <component
          v-bind:is="items[tab].content"
          :key="tab"
          :id="user_id"
        ></component>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import MyComments from "@/components/MyComments.vue";
import MyProfile from "@/components/MyProfile.vue";
import MyReviews from "@/components/MyReviews.vue";
import MyWatchlist from "@/components/MyWatchlist.vue";
import MyFavorites from "@/components/MyFavorites.vue";
import MyFollowing from "@/components/MyFollowing.vue";
import MyFollowers from "@/components/MyFollowers.vue";
import TasteGroup from "@/components/TasteGroup.vue";

export default {
  components: {
    MyComments,
    MyProfile,
    MyReviews,
    MyWatchlist,
    MyFavorites,
    MyFollowing,
    MyFollowers,
    TasteGroup,
  },
  props: {
    id: { required: false },
  },
  data() {
    return {
      tab: 0,
      tabs: [
        { tab: "Profile", content: MyProfile, private: false },
        { tab: "Following", content: MyFollowing, private: false },
        { tab: "Followers", content: MyFollowers, private: false },
        { tab: "Comments", content: MyComments, private: false },
        { tab: "Reviews", content: MyReviews, private: false },
        { tab: "Watchlist", content: MyWatchlist, private: false },
        { tab: "Favorites", content: MyFavorites, private: false },
        { tab: "Taste Group", content: TasteGroup, private: true },
      ],
    };
  },
  async created() {},
  computed: {
    ...mapGetters("auth", ["isLoggedIn", "getUser"]),
    items() {
      if (this.isLoggedIn && (this.getUser.id === this.id || !this.id)) {
        return this.tabs;
      } else return this.tabs.filter((obj) => obj.private == false);
    },
    user_id() {
      return this.id || this.getUser.id;
    },
  },
  methods: {},
};
</script>