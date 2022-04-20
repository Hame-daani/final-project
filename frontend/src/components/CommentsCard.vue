<template>
  <v-card v-if="!editing">
    <v-card-title>
      {{ me.user.username }}
    </v-card-title>
    <v-card-subtitle>
      {{ me.created_at | getDate }}
    </v-card-subtitle>
    <v-card-text>
      {{ me.text }}
    </v-card-text>
    <v-card-actions v-if="isLoggedIn && getUser.id === me.user.id">
      <v-btn color="info" @click="enableEditing">Edit</v-btn>
      <v-dialog v-model="dialog" persistent max-width="300">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="warning" dark v-bind="attrs" v-on="on"> Delete </v-btn>
        </template>
        <v-card>
          <v-card-title class="text-h5"> Deleting this comment </v-card-title>
          <v-card-text>Are you sure?</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="dialog = false">
              Cancel
            </v-btn>
            <v-btn color="green darken-1" text @click="deleteComment">
              Yes
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card-actions>
  </v-card>
  <comment-form
    v-else
    :comment="me"
    @cancel-editing="cancelEditing"
    @comment-submitted="update($event)"
  />
</template>

<script>
import { mapGetters } from "vuex";
import CommentForm from "./CommentForm.vue";
import CommentsService from "@/services/CommentsService";

export default {
  components: { CommentForm },
  props: {
    comment: {
      required: true,
    },
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn", "getUser"]),
  },
  data() {
    return {
      me: { ...this.comment },
      editing: false,
      dialog: false,
    };
  },
  methods: {
    enableEditing() {
      this.editing = true;
    },
    cancelEditing() {
      this.editing = false;
    },
    async update(text) {
      const payload = {
        text: text,
      };
      return CommentsService.update(this.me.id, payload)
        .then((data) => (this.me = data))
        .then(() => (this.editing = false))
        .catch((err) => console.log(err.reponse.data));
    },
    async deleteComment() {
      this.dialog = false;
      return CommentsService.delete(this.me.id)
        .then(() => this.$emit("comment-deleted", this.me.id))
        .catch((err) => console.log(err.response.data));
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