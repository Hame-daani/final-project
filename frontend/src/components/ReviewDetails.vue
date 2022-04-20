<template>
  <v-card>
    <loading-circular :flag="loading" />
    <template v-if="!loading && me && !editing">
      <v-card-title>{{ me.movie.title }}</v-card-title>
      <v-card-subtitle>{{ me.user.username }}</v-card-subtitle>
      <v-card-subtitle
        >created at: {{ me.created_at | getDate }}</v-card-subtitle
      >
      <v-card-subtitle v-if="isUpdated"
        >updated at: {{ me.updated_at | getDate }}</v-card-subtitle
      >
      <v-container>
        <label for="">Rating</label>
        <span class="text-caption mr-2">
          ({{ me.rating | decimalPlace }})
        </span>
        <v-rating
          v-model="me.rating"
          length="10"
          readonly
          half-increments
        ></v-rating>
      </v-container>
      <v-card-text>{{ me.text }}</v-card-text>
      <v-card-actions v-if="isLoggedIn && me.user.id == getUser.id">
        <v-btn color="info" @click="enableEditing">Edit</v-btn>
        <v-dialog v-model="dialog" persistent max-width="290">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="warning" dark v-bind="attrs" v-on="on">
              Delete
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="text-h5"> Deleting this review </v-card-title>
            <v-card-text>Are you sure?</v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click="dialog = false">
                Cancel
              </v-btn>
              <v-btn color="green darken-1" text @click="deleteReview">
                Yes
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-card-actions>
    </template>
    <template v-if="editing">
      <v-card-title>{{ me.movie.title }}</v-card-title>
      <v-card-subtitle>{{ me.user.username }}</v-card-subtitle>
      <review-form :review_data="me" @review-submited="updateReview($event)" />
      <v-btn color="yellow" @click="cancelEditing">Cancle</v-btn>
    </template>
  </v-card>
</template>

<script>
import LoadingCircular from "@/components/LoadingCircular.vue";
import ReviewForm from "@/components/ReviewForm.vue";
import ReviewsService from "@/services/ReviewsService";
import { mapGetters } from "vuex";

export default {
  components: { LoadingCircular, ReviewForm },
  props: { id: { required: true } },
  data() {
    return {
      me: {},
      loading: false,
      editing: false,
      dialog: false,
    };
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn", "getUser"]),
    isUpdated() {
      const a = new Date(this.me.created_at);
      const b = new Date(this.me.updated_at);
      return a.getTime() !== b.getTime();
    },
  },
  async created() {
    await this.loadReview();
  },
  methods: {
    async loadReview() {
      this.loading = true;
      return ReviewsService.getReview(this.id)
        .then((data) => (this.me = data))
        .then(() => {
          this.loading = false;
        })
        .catch((err) => alert(err.response.data));
    },
    async updateReview(review) {
      const payload = {
        id: this.id,
        text: review.text,
        rating: review.rating,
      };
      return ReviewsService.update(payload)
        .then((data) => (this.me = data))
        .then(() => (this.editing = false))
        .catch((err) => {
          console.log(err.response.data);
        });
    },
    enableEditing() {
      this.editing = true;
    },
    cancelEditing() {
      this.editing = false;
    },
    async deleteReview() {
      this.dialog = false;
      return ReviewsService.delete(this.id)
        .then(() =>
          this.$router.push({ name: "movie", params: { id: this.me.movie.id } })
        )
        .catch((err) => console.log(err.response.data));
    },
  },
  filters: {
    decimalPlace(num) {
      return parseFloat(num).toFixed(2);
    },
    getDate(timestamp) {
      const d = new Date(timestamp);
      return d.toLocaleString();
    },
  },
};
</script>

<style>
</style>