<template>
  <v-card class="my-3 pa-5" height="500" shaped :loading="loading">
    <template slot="progress">
      <v-progress-linear
        color="deep-purple"
        height="10"
        indeterminate
        rounded
      ></v-progress-linear>
    </template>
    <template v-if="!loading && me">
      <v-row>
        <v-col>
          <v-img :src="me.movie.poster" class="float-left" width="300" contain>
          </v-img>
        </v-col>
        <v-col class="d-flex flex-column justify-space-between pa-5" cols="8">
          <v-row>
            <v-col cols="10">
              <router-link
                :to="{ name: 'profile', params: { id: me.user.id } }"
                style="text-decoration: none; color: inherit"
              >
                <v-avatar>
                  <v-img :src="me.user.pic"></v-img>
                </v-avatar>
              </router-link>
              <span class="text-h7 pa-3">
                Review By
                <span class="red--text">
                  <router-link
                    :to="{ name: 'profile', params: { id: me.user.id } }"
                    style="text-decoration: none; color: inherit"
                  >
                    {{ me.user.first_name }} {{ me.user.last_name }}
                  </router-link>
                </span>
              </span>
            </v-col>
            <v-col v-if="isLoggedIn && me.user.id == getUser.id">
              <v-dialog v-model="editDialog" persistent max-width="700">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="info" dark v-bind="attrs" v-on="on" icon>
                    <v-icon> mdi-pencil </v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title class="d-flex justify-space-between">
                    {{ me.movie.title }}
                    <v-btn color="grey" @click="editDialog = false" icon>
                      <v-icon> mdi-cancel </v-icon>
                    </v-btn>
                  </v-card-title>
                  <v-card-subtitle>{{ me.user.username }}</v-card-subtitle>
                  <v-card-text>
                    <review-form
                      :review_data="me"
                      @review-submited="updateReview($event)"
                      :key="JSON.stringify(me)"
                    />
                  </v-card-text>
                </v-card>
              </v-dialog>
              <v-dialog v-model="deleteDialog" persistent max-width="290">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="error" dark v-bind="attrs" v-on="on" icon>
                    <v-icon> mdi-delete </v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title class="text-h5">
                    Deleting this review
                  </v-card-title>
                  <v-card-text>Are you sure?</v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="green darken-1"
                      text
                      @click="deleteDialog = false"
                    >
                      Cancel
                    </v-btn>
                    <v-btn color="green darken-1" text @click="deleteReview">
                      Yes
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-col>
          </v-row>
          <v-row>
            <span class="text-h4">
              <router-link
                :to="{ name: 'movie', params: { id: me.movie.id } }"
                style="text-decoration: none; color: inherit"
              >
                {{ me.movie.title }}
              </router-link>
              <span class="text-subtitle-2">{{ me.movie.year }}</span>
            </span>
          </v-row>
          <v-row>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-chip v-on="on" v-bind="attrs">
                  <v-rating
                    v-model="me.rating"
                    length="10"
                    readonly
                    size="15"
                    half-increments
                    dense
                  ></v-rating>
                </v-chip>
              </template>
              <span>{{ me.rating | decimalPlace }}</span>
            </v-tooltip>
          </v-row>
          <v-row
            ><span class="text-caption">
              Created at: {{ me.created_at | getDate }}
            </span></v-row
          >
          <v-row v-if="isUpdated"
            ><span class="text-caption">
              Updated at: {{ me.updated_at | getDate }}
            </span></v-row
          >

          <v-row><v-divider></v-divider></v-row>

          <v-row>
            <v-card-text style="white-space: pre-line">{{
              me.text
            }}</v-card-text>
          </v-row>

          <v-row><v-divider></v-divider></v-row>

          <v-row>
            <v-btn color="red" v-if="isLoggedIn && !isLiked" @click="like" icon>
              <v-icon> mdi-heart-outline </v-icon>
            </v-btn>
            <v-btn
              color="red"
              v-if="isLoggedIn && isLiked"
              @click="unlike"
              icon
            >
              <v-icon> mdi-heart </v-icon>
            </v-btn>
            <span class="overline red--text">
              <v-icon v-if="!isLoggedIn" color="red"> mdi-heart </v-icon>
              {{ this.likes.length }} Likes
            </span>
          </v-row>
        </v-col>
      </v-row>
    </template>
  </v-card>
</template>

<script>
import ReviewForm from "@/components/ReviewForm.vue";
import ReviewsService from "@/services/ReviewsService";
import LikesService from "@/services/LikesService";
import { mapGetters } from "vuex";

export default {
  components: { ReviewForm },
  props: { id: { required: true } },
  data() {
    return {
      me: {},
      likes: [],
      loading: false,
      editing: false,
      deleteDialog: false,
      editDialog: false,
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
        .then(() => (this.editDialog = false))
        .catch((err) => {
          console.log(err.response.data);
        });
    },
    async deleteReview() {
      this.deleteDialog = false;
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