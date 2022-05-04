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
      <v-card-title> My Taste Group </v-card-title>
      <v-divider></v-divider>
      <v-row>
        <v-col v-for="user in users" :key="user.id">
          <user-preview :user="user" />
        </v-col>
      </v-row>
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
import UserPreview from "@/components/UserPreview.vue";

export default {
  components: {
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