<template>
  <v-card>
    <loading-circular :flag="loading" />
    <v-card-title>{{ movie.title }}</v-card-title>
    <v-card-subtitle>{{ movie.year }}</v-card-subtitle>
    <v-card-subtitle> Num Likes: {{ this.likes.length }} </v-card-subtitle>
    <v-card-subtitle>
      Num wathclist: {{ this.watchlist.length }}
    </v-card-subtitle>
    <v-img aspect-ratio="1.7" :src="movie.poster" contain />
    <iframe
      src="https://www.imdb.com/video/imdb/vi2959588889/imdb/embed?autoplay=false&amp;width=640"
      allowfullscreen="true"
      mozallowfullscreen="true"
      webkitallowfullscreen="true"
      scrolling="no"
      width="640"
      height="360"
      frameborder="no"
    ></iframe>
    <v-container>
      <label for="">Average Rating</label>
      <span class="text-caption mr-2">
        ({{ movie.avg_rating | decimalPlace }})
      </span>
      <v-rating
        v-model="movie.avg_rating"
        length="10"
        readonly
        half-increments
      ></v-rating>
    </v-container>
    <v-container v-show="isLoggedIn">
      <label for="">Estimated Rating</label>
      <span class="text-caption mr-2">
        ({{ movie.estimated_rating | decimalPlace }})
      </span>
      <v-rating
        v-model="movie.estimated_rating"
        length="10"
        readonly
        half-increments
      ></v-rating>
    </v-container>
    <v-card-actions>
      <v-btn v-if="!isLiked" color="info" @click="like">Like</v-btn>
      <v-btn v-if="isLiked" color="info" @click="unlike">Unlike</v-btn>
      <v-btn v-if="!isWathclisted" color="info" @click="addWatchlist"
        >Add to Watchlist</v-btn
      >
      <v-btn v-if="isWathclisted" color="info" @click="removeWatchlist"
        >Remove from Watchlist</v-btn
      >
    </v-card-actions>
    <v-card-text>{{ movie.plot }}</v-card-text>
  </v-card>
</template>

<script>
import MoviesService from "@/services/MoviesService";
import { mapGetters } from "vuex";
import LoadingCircular from "@/components/LoadingCircular.vue";
import LikesService from "@/services/LikesService";

export default {
  name: "MovieView",
  components: { LoadingCircular },
  props: { id: { required: true } },
  data() {
    return {
      movie: {},
      likes: [],
      watchlist: [],
      loading: false,
    };
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn", "getUser"]),
    isLiked() {
      return this.likes.find((obj) => obj.user.id === this.getUser.id);
    },
    isWathclisted() {
      return this.watchlist.find((obj) => obj.id === this.getUser.id);
    },
  },
  async created() {
    await this.loadMovie();
    this.loadLikes();
    this.loadWatchlists();
  },
  methods: {
    async loadMovie() {
      this.loading = true;
      return MoviesService.getMovie(this.id)
        .then((data) => (this.movie = data))
        .then(() => (this.loading = false))
        .catch((err) => alert(err.response.data));
    },
    async loadLikes() {
      return LikesService.getLikes("movies/", this.movie.id)
        .then((data) => (this.likes = data))
        .catch((err) => console.log(err.reponse.data));
    },
    async like() {
      return LikesService.addLike("movies/", this.movie.id)
        .then(() => this.loadLikes())
        .catch((err) => console.log(err.reponse.data));
    },
    async unlike() {
      return LikesService.deleteLike(this.isLiked.id)
        .then(() => this.loadLikes())
        .catch((err) => console.log(err.reponse.data));
    },
    async loadWatchlists() {
      return MoviesService.getWatchlists(this.movie.id)
        .then((data) => (this.watchlist = data))
        .catch((err) => console.log(err.reponse.data));
    },
    async addWatchlist() {
      return MoviesService.addToWatchlist(this.movie.id)
        .then(() => this.loadWatchlists())
        .catch((err) => console.log(err.reponse.data));
    },
    async removeWatchlist() {
      return MoviesService.removeFromWatchlist(this.movie.id)
        .then(() => this.loadWatchlists())
        .catch((err) => console.log(err.reponse.data));
    },
  },
  filters: {
    decimalPlace(num) {
      return parseFloat(num).toFixed(2);
    },
  },
};
</script>

<style>
</style>