<template>
  <v-card
    class="mx-auto my-3 pa-5"
    :to="{ name: 'profile', params: { id: me.id } }"
    shaped
    width="700"
    elevation="3"
  >
    <v-row>
      <v-col cols="2">
        <!-- pic -->
        <v-avatar size="100">
          <v-img :src="me.pic"></v-img>
        </v-avatar>
      </v-col>
      <v-col><v-divider vertical></v-divider></v-col>
      <v-col class="d-flex flex-column align-center my-7" cols="5">
        <!-- info -->
        <v-row>
          <span class="text-h6">{{ me.first_name }} {{ me.last_name }}</span>
        </v-row>
        <v-row>
          <span class="text-subtitle-2 mr-3">{{ following }} following </span>
          <span class="text-subtitle-2">{{ followers }} followers</span>
        </v-row>
      </v-col>
      <v-col><v-divider vertical></v-divider></v-col>
      <v-col class="my-7" cols="4">
        <!-- icons -->
        <v-row>
          <span class="ma-3 text-caption">
            {{ watched }}
            <v-icon color="green"> mdi-eye </v-icon>
          </span>
          <span class="ma-3 text-caption">
            {{ favorites }}
            <v-icon color="red"> mdi-heart </v-icon>
          </span>
          <span class="ma-3 text-caption">
            {{ watchlist }}
            <v-icon color="grey"> mdi-clock </v-icon>
          </span>
        </v-row>
        <v-row v-if="similarity">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip v-on="on" v-bind="attrs" color="yellow">
                <v-rating
                  v-model="similarity"
                  length="10"
                  size="5"
                  small
                  dense
                  half-increments
                  readonly
                />
              </v-chip>
            </template>
            <span>Similarity: {{ me.similarity }}</span>
          </v-tooltip>
        </v-row>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import UsersService from "@/services/UsersService";
export default {
  props: {
    user: { required: true },
  },
  data() {
    return {
      me: this.user,
      following: 0,
      followers: 0,
      watched: 0,
      favorites: 0,
      watchlist: 0,
    };
  },
  async created() {
    this.loadData();
  },
  computed: {
    similarity() {
      return this.me.similarity * 5 + 5;
    },
  },
  methods: {
    async loadData() {
      UsersService.getExtras(this.me.id)
        .then((data) => {
          this.following = data.following;
          this.followers = data.followers;
          this.watched = data.watched;
          this.watchlist = data.watchlist;
          this.favorites = data.favorites;
        })
        .catch((err) => console.log(err.reponse.data));
    },
  },
};
</script>

<style>
</style>