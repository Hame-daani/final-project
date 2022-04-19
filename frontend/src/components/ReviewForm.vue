<template>
  <v-container>
    <template>
      <v-form ref="form">
        <v-text-field
          label="text"
          v-model="review.text"
          :rules="rules"
          hide-details="auto"
          clearable
          required
        ></v-text-field>
        <v-rating
          v-model="review.rating"
          ref="rating"
          length="10"
          hover
          clearable
          required
        ></v-rating>
        <v-btn @click="submit"> submit </v-btn>
        <v-btn @click="clear">clear</v-btn>
      </v-form>
    </template>
  </v-container>
</template>

<script>
export default {
  props: {
    review_data: { required: false },
  },
  data() {
    return {
      review: this.review || { text: "", rating: 0 },
      rules: [
        (value) => !!value || "Required.",
        // (value) => (value && value.length >= 3) || "Min 3 characters",
      ],
    };
  },
  methods: {
    submit() {
      if (this.$refs.form.validate())
        this.$emit("review-submited", this.review);
    },
    clear() {
      this.$refs.form.reset();
      this.review.rating = 0;
    },
  },
};
</script>

<style>
</style>