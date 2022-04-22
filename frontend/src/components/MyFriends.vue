<template>
  <v-container>
    <v-card>
      <v-card-title> My Friends </v-card-title>
      <loading-circular :flag="loading" />
      <user-preview v-for="user in friends" :key="user.id" :user="user" />
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
import LoadingCircular from "@/components/LoadingCircular.vue";
import UserPreview from "@/components/UserPreview.vue";

export default {
  components: {
    LoadingCircular,
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
      friends: [],
      page: 1,
      total_pages: 1,
      loading: false,
    };
  },
  methods: {
    async loadData() {
      this.loading = true;
      this.friends = [];
      const payload = {
        params: {
          page: this.page,
        },
      };
      return UsersService.getFriends(this.id, payload)
        .then((data) => {
          this.friends = data.results;
          this.total_pages = data.total_pages;
        })
        .then(() => (this.loading = false))
        .catch((err) => console.log(err.reponse.data));
    },
  },
};
</script>

<style>
</style>