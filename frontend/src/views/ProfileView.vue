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
import UsersService from "@/services/UsersService";

export default {
  components: {
    MyComments,
    MyProfile,
    MyReviews,
    MyWatchlist,
    MyFavorites,
  },
  props: {
    id: { required: true },
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
      ],
      user: {},
    };
  },
  async created() {
    this.loadData();
  },
  computed: { ...mapGetters("auth", ["isLoggedIn"]) },
  methods: {
    async loadData() {
      return UsersService.getUser(this.id)
        .then((data) => (this.user = data))
        .catch((err) => console.log(err.response.data));
    },
  },
};
</script>