<template>
  <v-card
    class="mx-auto my-3 pa-5"
    width="400"
    :to="{ name: 'review', params: { id: me.id } }"
  >
    <v-row v-if="showMovie">
      <v-col>
        <v-img
          :src="me.movie.poster"
          class="float-left"
          width="130"
          contain
        ></v-img>
      </v-col>
      <v-col cols="7" class="d-flex flex-column justify-space-between">
        <v-row>
          <v-avatar>
            <v-img
              src="https://randomuser.me/api/portraits/women/85.jpg"
            ></v-img>
          </v-avatar>
          <span class="text-subtitle-2 ma-3">
            {{ me.user.first_name }}
          </span>
        </v-row>
        <v-row class="text-h6">{{ me.movie.title }}</v-row>
        <v-row
          ><v-rating v-model="me.rating" length="10" small dense readonly
        /></v-row>
      </v-col>
    </v-row>
    <template v-else>
      <v-card-title
        ><v-avatar>
          <v-img src="https://randomuser.me/api/portraits/women/85.jpg"></v-img>
        </v-avatar>
        <span class="text-subtitle-2 ma-3">
          {{ me.user.first_name }}
        </span></v-card-title
      >
      <v-card-subtitle>
        <v-rating v-model="me.rating" length="10" small dense readonly
      /></v-card-subtitle>
    </template>
    <v-card-text>
      {{ me.text }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    review: { required: true },
    showMovie: { type: Boolean, default: true },
  },
  data() {
    return { me: this.review };
  },
};
</script>

<style>
</style>