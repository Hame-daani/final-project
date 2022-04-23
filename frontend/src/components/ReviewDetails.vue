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
      <v-card-subtitle> Num Likes: {{ this.likes.length }} </v-card-subtitle>
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
      <v-card-actions v-if="isLoggedIn">
        <v-btn v-if="!isLiked" color="info" @click="like">Like</v-btn>
        <v-btn v-if="isLiked" color="info" @click="unlike">Unlike</v-btn>
        <template v-if="me.user.id == getUser.id">
          <v-btn color="info" @click="enableEditing">Edit</v-btn>
          <v-dialog v-model="dialog" persistent max-width="290">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="warning" dark v-bind="attrs" v-on="on">
                Delete
              </v-btn>
            </template>
            <v-card>
              <v-card-title class="text-h5">
                Deleting this review
              </v-card-title>
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
        </template>
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
import LikesService from "@/services/LikesService";
import { mapGetters } from "vuex";

export default {
  components: { LoadingCircular, ReviewForm },
  props: { id: { required: true } },
  data() {
    return {
      me: {},
      likes: [],
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
    isLiked() {
      return this.likes.find((obj) => obj.user.id === this.getUser.id);
    },
  },
  async created() {
    await this.loadReview();
    this.loadLikes();
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
    async loadLikes() {
      return LikesService.getLikes("reviews/", this.me.id)
        .then((data) => (this.likes = data))
        .catch((err) => console.log(err.reponse.data));
    },
    async like() {
      return LikesService.addLike("reviews/", this.me.id)
        .then(() => this.loadLikes())
        .catch((err) => console.log(err.reponse.data));
    },
    async unlike() {
      return LikesService.deleteLike(this.isLiked.id)
        .then(() => this.loadLikes())
        .catch((err) => console.log(err.reponse.data));
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