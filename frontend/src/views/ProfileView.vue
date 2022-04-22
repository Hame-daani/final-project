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
          :user="user"
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
import MyFriends from "@/components/MyFriends.vue";
import TasteGroup from "@/components/TasteGroup.vue";
import MyReqs from "@/components/MyReqs.vue";
import UsersService from "@/services/UsersService";

export default {
  components: {
    MyComments,
    MyProfile,
    MyReviews,
    MyWatchlist,
    MyFavorites,
    MyFriends,
    TasteGroup,
    MyReqs,
  },
  props: {
    id: { required: false },
  },
  data() {
    return {
      tab: 0,
      tabs: [
        { tab: "Profile", content: MyProfile, private: false },
        { tab: "Friends", content: MyFriends, private: false },
        { tab: "Comments", content: MyComments, private: false },
        { tab: "Reviews", content: MyReviews, private: false },
        { tab: "Watchlist", content: MyWatchlist, private: false },
        { tab: "Favorites", content: MyFavorites, private: false },
        { tab: "Friend Requests", content: MyReqs, private: true },
        { tab: "Taste Group", content: TasteGroup, private: true },
      ],
      user: {},
    };
  },
  async created() {
    if (this.id) this.loadData();
    else if (this.isLoggedIn) this.user = this.getUser;
    else this.$router.push({ name: "login" });
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn", "getUser"]),
    items() {
      if (this.isLoggedIn && (this.getUser.id === this.id || !this.id)) {
        return this.tabs;
      } else return this.tabs.filter((obj) => obj.private == false);
    },
  },
  methods: {
    async loadData() {
      return UsersService.getUser(this.id)
        .then((data) => (this.user = data))
        .catch((err) => console.log(err.response.data));
    },
    async logout() {
      return this.$store
        .dispatch("auth/logout")
        .then(() => this.$router.push({ name: "login" }))
        .catch((err) => alert(err.response.data));
    },
  },
};
</script>