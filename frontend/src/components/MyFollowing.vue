<template>
  <v-container>
    <v-card flat :loading="loading">
      <template slot="progress">
        <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
          rounded
        ></v-progress-linear>
      </template>
      <v-card-title>
        <v-badge color="green" :content="count"> My Followings </v-badge>
      </v-card-title>

      <v-divider></v-divider>
      <user-preview
        class="my-5"
        v-for="user in following"
        :key="user.id"
        :user="user"
      />
    </v-card>
    <v-pagination
      v-model="page"
      class="my-4"
      :length="total_pages"
      @input="loadData"
    />
  </v-container>
</template>

<script>
import UsersService from "@/services/UsersService";
import UserPreview from "@/components/UserPreview.vue";

export default {
  components: {
    UserPreview,
  },
  props: {
    id: { required: true },
  },
  async created() {
    return this.loadData();
  },
  data() {
    return {
      following: [],
      page: 1,
      total_pages: 1,
      count: 0,
      loading: false,
    };
  },
  methods: {
    async loadData() {
      this.loading = true;
      this.following = [];
      const payload = {
        params: {
          page: this.page,
        },
      };
      return UsersService.getfollowing(this.id, payload)
        .then((data) => {
          this.following = data.results;
          this.total_pages = data.total_pages;
          this.count = data.count;
        })
        .then(() => (this.loading = false))
        .catch((err) => console.log(err.reponse.data));
    },
  },
};
</script>

<style>
</style>