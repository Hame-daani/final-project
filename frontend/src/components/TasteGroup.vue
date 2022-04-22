<template>
  <v-container>
    <v-card>
      <v-card-title> My Taste Group </v-card-title>
      <loading-circular :flag="loading" />
      <user-preview v-for="user in users" :key="user.id" :user="user" />
    </v-card>
    <v-pagination
      v-model="page"
      class="my-4"
      :length="total_pages"
      @input="loadUsers"
    />
  </v-container>
</template>

<script>
import RecommenderService from "@/services/RecommenderService";
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
    return this.loadUsers();
  },
  data() {
    return {
      users: [],
      page: 1,
      total_pages: 1,
      loading: false,
    };
  },
  methods: {
    async loadUsers() {
      this.loading = true;
      this.users = [];
      const payload = {
        params: {
          page: this.page,
        },
      };
      return RecommenderService.getTasteGroup(payload)
        .then((data) => {
          this.users = data.results;
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