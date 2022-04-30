<template>
  <v-container>
    <v-card shaped>
      <v-toolbar flat color="blue-grey" dark>
        <v-tabs
          v-model="tab"
          fixed-tabs
          align-with-title
          active-class="yellow--text"
        >
          <v-tab
            v-for="item in items"
            :key="item.tab"
            class="d-flex flex-column justify-space-around"
          >
            <v-icon>{{ item.icon }}</v-icon>
            {{ item.tab }}
          </v-tab>
        </v-tabs>
      </v-toolbar>
      <v-container class="pa-10">
        <component
          v-bind:is="items[tab].content"
          :key="tab"
          :id="user_id"
        ></component>
      </v-container>
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
        {
          tab: "Profile",
          content: MyProfile,
          private: false,
          icon: "mdi-account",
        },
        {
          tab: "Following",
          content: MyFollowing,
          private: false,
          icon: "mdi-account-multiple",
        },
        {
          tab: "Followers",
          content: MyFollowers,
          private: false,
          icon: "mdi-account-group",
        },
        {
          tab: "Comments",
          content: MyComments,
          private: false,
          icon: "mdi-comment-multiple",
        },
        {
          tab: "Reviews",
          content: MyReviews,
          private: false,
          icon: "mdi-note-multiple",
        },
        {
          tab: "Watchlist",
          content: MyWatchlist,
          private: false,
          icon: "mdi-clock",
        },
        {
          tab: "Favorites",
          content: MyFavorites,
          private: false,
          icon: "mdi-heart",
        },
        {
          tab: "Taste Group",
          content: TasteGroup,
          private: true,
          icon: "mdi-account-multiple-plus",
        },
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