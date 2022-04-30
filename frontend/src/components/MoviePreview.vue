<template>
  <v-card
    class="mx-auto my-3 pa-5"
    width="400"
    :to="{ name: 'movie', params: { id: me.id } }"
    shaped
    elevation="3"
  >
    <v-row>
      <v-col>
        <!-- img -->
        <v-img :src="me.poster" class="float-left" width="130" contain></v-img>
      </v-col>
      <v-col class="d-flex flex-column" cols="7">
        <!-- detail -->
        <v-row>
          <span class="text-h6">{{ me.title }}</span>
        </v-row>
        <v-row>
          <span class="text-caption">{{ me.year }}</span>
        </v-row>
        <v-row>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip v-on="on" v-bind="attrs">
                <v-rating
                  v-model="me.avg_rating"
                  length="10"
                  size="5"
                  small
                  dense
                  half-increments
                  readonly
                />
              </v-chip>
            </template>
            <span>Average Rating: {{ me.avg_rating | decimalPlace }}</span>
          </v-tooltip>
        </v-row>
        <v-row v-if="me.estimated_rating">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip v-on="on" v-bind="attrs">
                <v-rating
                  v-model="me.estimated_rating"
                  length="10"
                  size="5"
                  small
                  dense
                  half-increments
                  readonly
                />
              </v-chip>
            </template>
            <span
              >Estimated Rating {{ me.estimated_rating | decimalPlace }}</span
            >
          </v-tooltip>
        </v-row>
        <v-row v-if="me.similarity">
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
export default {
  props: { movie: { required: true } },
  data() {
    return {
      me: this.movie,
    };
  },
  computed: {
    similarity() {
      return this.me.similarity * 5 + 5;
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