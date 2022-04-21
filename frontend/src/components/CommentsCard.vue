<template>
  <v-container>
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
      <v-card-actions v-if="isLoggedIn">
        <v-btn color="info" @click="replying = true">Reply</v-btn>
        <template v-if="getUser.id === me.user.id">
          <v-btn color="info" @click="editing = true">Edit</v-btn>
          <v-dialog v-model="deleteDialog" persistent max-width="300">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="warning" dark v-bind="attrs" v-on="on">
                Delete
              </v-btn>
            </template>
            <v-card>
              <v-card-title class="text-h5">
                Deleting this comment
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
                <v-btn color="green darken-1" text @click="deleteComment">
                  Yes
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </template>
      </v-card-actions>
    </v-card>
    <comment-form
      v-else
      :comment="me"
      :editing="true"
      @cancel="editing = false"
      @comment-submitted="update($event)"
    />
    <comment-form
      v-if="replying"
      :replying="true"
      @cancel="replying = false"
      @comment-submitted="reply($event)"
    />
  </v-container>
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
      replying: false,
      deleteDialog: false,
    };
  },
  methods: {
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
      this.deleteDialog = false;
      return CommentsService.delete(this.me.id)
        .then(() => this.$emit("comment-deleted", this.me.id))
        .catch((err) => console.log(err.response.data));
    },
    async reply(text) {
      const payload = {
        text: text,
      };
      return CommentsService.addComment(this.me.id, payload)
        .then((data) => this.me.comments.push(data))
        .then(() => (this.replying = false))
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