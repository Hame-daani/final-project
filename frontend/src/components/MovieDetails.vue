<template>
  <v-card class="my-3 pa-10" shaped :loading="loading">
    <template slot="progress">
      <v-progress-linear
        color="deep-purple"
        height="10"
        indeterminate
        rounded
      ></v-progress-linear>
    </template>
    <v-row>
      <v-row>
        <v-col cols="4">
          <!-- poster -->
          <v-row>
            <v-img
              :src="movie.poster"
              class="float-left"
              height="400"
              contain
            />
          </v-row>
          <v-row class="d-flex justify-center">
            <span class="ma-3 text-caption">
              <v-icon color="green"> mdi-eye </v-icon>
              {{ reviewCounts }}
            </span>
            <span class="ma-3 text-caption">
              <v-dialog v-model="likesDialog" persistent max-width="700">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon color="red" v-bind="attrs" v-on="on">
                    mdi-heart
                  </v-icon>
                  {{ likes.length }}
                </template>
                <v-card>
                  <v-card-title>
                    <v-row class="d-flex justify-space-between pa-5">
                      <span> Liked by: </span>
                      <v-btn color="grey" @click="likesDialog = false" icon>
                        <v-icon> mdi-cancel </v-icon>
                      </v-btn>
                    </v-row>
                  </v-card-title>
                  <v-card-text>
                    <v-virtual-scroll
                      :bench="2"
                      :items="likes"
                      height="300"
                      item-height="64"
                    >
                      <template v-slot:default="{ item }">
                        <v-list-item>
                          <v-list-item-avatar>
                            <v-avatar size="56" class="white--text">
                              <v-img :src="item.user.pic"> </v-img>
                            </v-avatar>
                          </v-list-item-avatar>

                          <v-list-item-content>
                            <v-list-item-title>{{
                              item.user.username
                            }}</v-list-item-title>
                          </v-list-item-content>

                          <v-list-item-action>
                            <v-btn
                              depressed
                              small
                              :to="{
                                name: 'profile',
                                params: { id: item.user.id },
                              }"
                            >
                              View User

                              <v-icon color="orange darken-4" right>
                                mdi-open-in-new
                              </v-icon>
                            </v-btn>
                          </v-list-item-action>
                        </v-list-item>
                        <v-divider></v-divider>
                      </template>
                    </v-virtual-scroll>
                  </v-card-text>
                </v-card>
              </v-dialog>
            </span>
            <span class="ma-3 text-caption">
              <v-dialog v-model="watchlistDialog" persistent max-width="700">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon color="grey" v-bind="attrs" v-on="on">
                    mdi-clock
                  </v-icon>
                  {{ watchlist.length }}
                </template>
                <v-card>
                  <v-card-title>
                    <v-row class="d-flex justify-space-between pa-5">
                      <span> Watchlisted by: </span>
                      <v-btn color="grey" @click="watchlistDialog = false" icon>
                        <v-icon> mdi-cancel </v-icon>
                      </v-btn>
                    </v-row>
                  </v-card-title>
                  <v-card-text>
                    <v-virtual-scroll
                      :bench="2"
                      :items="watchlist"
                      height="300"
                      item-height="64"
                    >
                      <template v-slot:default="{ item }">
                        <v-list-item>
                          <v-list-item-avatar>
                            <v-avatar size="56" class="white--text">
                              <v-img :src="item.pic"> </v-img>
                            </v-avatar>
                          </v-list-item-avatar>

                          <v-list-item-content>
                            <v-list-item-title>{{
                              item.username
                            }}</v-list-item-title>
                          </v-list-item-content>

                          <v-list-item-action>
                            <v-btn
                              depressed
                              small
                              :to="{ name: 'profile', params: { id: item.id } }"
                            >
                              View User

                              <v-icon color="orange darken-4" right>
                                mdi-open-in-new
                              </v-icon>
                            </v-btn>
                          </v-list-item-action>
                        </v-list-item>
                        <v-divider></v-divider>
                      </template>
                    </v-virtual-scroll>
                  </v-card-text>
                </v-card>
              </v-dialog>
            </span>
          </v-row>
          <v-row class="d-flex justify-center align-center">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-chip v-on="on" v-bind="attrs">
                  <span class="text-h7">Average Rating: </span>
                  <v-rating
                    v-model="movie.avg_rating"
                    length="10"
                    size="15"
                    color="red"
                    readonly
                    dense
                    half-increments
                  />
                </v-chip>
              </template>
              <span>{{ movie.avg_rating | decimalPlace }}</span>
            </v-tooltip>
          </v-row>
          <v-row
            v-if="movie.estimated_rating"
            class="d-flex justify-center align-center mt-5"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-chip v-on="on" v-bind="attrs">
                  <span class="text-h7">Estimated Rating: </span>
                  <v-rating
                    v-model="movie.estimated_rating"
                    length="10"
                    size="15"
                    color="blue"
                    readonly
                    dense
                    half-increments
                  />
                </v-chip>
              </template>
              <span>{{ movie.estimated_rating | decimalPlace }}</span>
            </v-tooltip>
          </v-row>
        </v-col>
        <v-col cols="8">
          <v-row>
            <v-col>
              <!-- detail -->
              <v-row>
                <span class="text-h4">
                  {{ movie.title }}
                  <span class="text-subtitle-2"> {{ movie.year }} </span>
                </span>
              </v-row>
              <v-row class="pa-3">
                <v-chip class="me-1" v-for="genre in movie.genres" :key="genre">
                  {{ genre }}
                </v-chip>
              </v-row>
              <v-row class="ma-3">
                <span class="text-body-1"> {{ movie.plot }} </span>
              </v-row>
            </v-col>
            <v-col class="d-flex flex-column justify-start" cols="1">
              <!-- icons -->
              <!-- like -->
              <v-btn
                color="red"
                v-if="isLoggedIn && !isLiked"
                @click="like"
                icon
              >
                <v-icon size="50"> mdi-heart-outline </v-icon>
              </v-btn>
              <v-btn
                color="red"
                v-if="isLoggedIn && isLiked"
                @click="unlike"
                icon
              >
                <v-icon size="50"> mdi-heart </v-icon>
              </v-btn>
              <!-- watchlist -->
              <v-btn
                class="mt-3"
                color="grey"
                v-if="isLoggedIn && !isWathclisted"
                @click="addWatchlist"
                icon
              >
                <v-icon size="50">mdi-clock-outline</v-icon>
              </v-btn>
              <v-btn
                class="mt-3"
                color="grey"
                v-if="isLoggedIn && isWathclisted"
                @click="removeWatchlist"
                icon
              >
                <v-icon size="50">mdi-clock</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row class="d-flex ma-1">
            <!-- trailer -->
            <v-card class="flex-grow-1" elevation="3">
              <v-card-title> Trailer </v-card-title>
              <v-container class="d-flex justify-center">
                <iframe
                  src="https://www.imdb.com/video/imdb/vi2959588889/imdb/embed?autoplay=false&amp;width=480"
                  allowfullscreen="true"
                  mozallowfullscreen="true"
                  webkitallowfullscreen="true"
                  scrolling="no"
                  width="480"
                  height="260"
                  frameborder="no"
                />
              </v-container>
            </v-card>
          </v-row>
        </v-col>
      </v-row>
    </v-row>
  </v-card>
</template>

<script>
import MoviesService from "@/services/MoviesService";
// import UserPreview from "@/components/UserPreview";
import { mapGetters } from "vuex";
import LikesService from "@/services/LikesService";

export default {
  name: "MovieView",
  // components: { UserPreview },
  props: { id: { required: true }, reviewCounts: { required: true } },
  data() {
    return {
      movie: {},
      likes: [],
      watchlist: [],
      loading: false,
      watchlistDialog: false,
      likesDialog: false,
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
        .then((data) => {
          this.likes = data;
          console.log(this.likes);
        })
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