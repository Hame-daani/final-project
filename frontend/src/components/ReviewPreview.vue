<template>
  <v-card
    class="mx-auto my-3"
    max-width="400"
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
        <v-row class="text-subtitle-2">{{ me.movie.title }} </v-row>
        <v-row class="text-h5">{{ me.user.username }}</v-row>
        <v-row
          ><v-rating v-model="me.rating" length="10" small dense readonly
        /></v-row>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-row class="">{{ me.movie.title }} </v-row>
      <v-row>{{ me.user.username }}</v-row>
      <v-row
        ><v-rating v-model="me.rating" length="10" small dense readonly
      /></v-row>
    </v-row>
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