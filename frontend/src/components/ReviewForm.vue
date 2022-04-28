<template>
  <v-container>
    <v-form ref="form">
      <v-textarea
        label="text"
        v-model="review.text"
        :rules="rules"
        hide-details="auto"
        multiline
        filled
        clearable
        required
      ></v-textarea>
      <v-rating
        v-model="review.rating"
        ref="rating"
        length="10"
        hover
        clearable
        required
      ></v-rating>
      <v-btn @click="submit" color="green" icon>
        <v-icon>mdi-send</v-icon>
      </v-btn>
      <v-btn @click="clear" color="red" icon>
        <v-icon>mdi-backspace</v-icon>
      </v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  props: {
    review_data: {
      required: false,
      default() {
        return { text: "", rating: 0 };
      },
    },
  },
  data() {
    return {
      review: { ...this.review_data },
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