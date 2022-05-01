<template>
  <v-card v-if="!editing" flat :loading="loading">
    <template slot="progress">
      <v-progress-linear
        color="deep-purple"
        height="10"
        indeterminate
        rounded
      ></v-progress-linear>
    </template>
    <!-- profile detail -->
    <v-row class="d-flex flex-row">
      <v-col class="pa-5" cols="3">
        <!-- pic -->
        <v-avatar size="200" tile>
          <v-img :src="me.pic"></v-img>
        </v-avatar>
      </v-col>
      <v-col class="d-flex flex-column mt-7">
        <!-- detail -->
        <v-row>
          <span class="text-h5 mr-3">{{ me.username }}</span>
          <v-chip class="ml-1 white--text" v-if="isfollows" color="green">
            Follows You
          </v-chip>
          <v-chip class="ml-1 white--text" v-if="isfollowing" color="purple">
            Following
          </v-chip>
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
        <v-row>
          First Name:
          <span class="text-subtitle-2 ml-2">{{ me.first_name }} </span>
        </v-row>
        <v-row>
          Last Name:
          <span class="text-subtitle-2 ml-2">{{ me.last_name }} </span>
        </v-row>
        <v-row>
          Date Joined:
          <span class="text-subtitle-2 ml-2">
            {{ me.date_joined | getDate }}
          </span>
        </v-row>
        <v-row>
          Gender: <span class="text-subtitle-2 ml-2">{{ me.gender }} </span>
        </v-row>
      </v-col>
      <v-col v-if="isLoggedIn && !isThisMe" cols="2">
        <!-- buttons -->
        <v-tooltip bottom v-if="isfollowing">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="red"
              rounded
              @click="unfollow"
              v-on="on"
              v-bind="attrs"
            >
              <v-icon> mdi-account-minus </v-icon>
            </v-btn>
          </template>
          <span>Unfollow</span>
        </v-tooltip>
        <v-tooltip v-else bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="blue"
              rounded
              @click="follow"
              v-on="on"
              v-bind="attrs"
            >
              <v-icon> mdi-account-plus </v-icon>
            </v-btn>
          </template>
          <span>Follow</span>
        </v-tooltip>
      </v-col>
      <v-col v-else-if="isThisMe" cols="1">
        <v-btn color="blue" @click="enableEditing" icon>
          <v-icon> mdi-pencil </v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-card>
  <v-card v-else>
    <!-- edit profile -->
    <v-card-title> Editing Your Info </v-card-title>
    <template>
      <v-row class="d-flex justify-space-around">
        <v-col cols="3">
          <!-- pic -->
          <v-file-input
            accept="image/*"
            label="Select you avatar"
          ></v-file-input>
        </v-col>
        <v-col cols="7">
          <!-- info -->
          <v-form ref="form" v-model="valid" lazy-validation> </v-form>
          <v-row>
            <v-text-field
              name="firstname"
              v-model="me.first_name"
              label="First Name"
              required
            ></v-text-field>
          </v-row>
          <v-row>
            <v-text-field
              name="lastname"
              v-model="me.last_name"
              label="Last Name"
              required
            ></v-text-field>
          </v-row>
          <v-row>
            <v-text-field
              name="email"
              v-model="me.email"
              label="Email"
              required
            ></v-text-field>
          </v-row>
        </v-col>
        <v-col class="d-flex flex-column justify-space-around" cols="1">
          <v-btn color="green" @click="update" icon>
            <v-icon> mdi-send </v-icon>
          </v-btn>
          <v-btn color="red" @click="clear" icon>
            <v-icon> mdi-backspace </v-icon>
          </v-btn>
          <v-btn color="grey" @click="cancel" icon>
            <v-icon> mdi-cancel </v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </v-card>
</template>

<script>
import UsersService from "@/services/UsersService";
import { mapGetters } from "vuex";

export default {
  props: {
    id: { required: true },
  },
  computed: {
    ...mapGetters("auth", ["isLoggedIn", "getUser"]),
    isThisMe() {
      return this.getUser.id === this.id;
    },
    similarity() {
      return this.me.similarity * 5 + 5;
    },
  },
  data() {
    return {
      me: {},
      valid: true,
      loading: false,
      editing: false,
      isfollowing: false,
      isfollows: false,
    };
  },
  async created() {
    if (!this.id || this.id === this.getUser.id) this.me = this.getUser;
    else await this.loadData();
    if (this.isLoggedIn && this.id !== this.getUser.id) this.loadFriendship();
  },
  methods: {
    async loadData() {
      this.loading = true;
      return UsersService.getUser(this.id)
        .then((data) => (this.me = data))
        .then(() => (this.loading = false))
        .catch((err) => console.log(err.reponse.data));
    },
    async loadFriendship() {
      UsersService.isfollowing(this.me.id)
        .then((data) => {
          this.isfollowing = data.result;
        })
        .catch((err) => console.log(err.reponse.data));
      UsersService.isfollows(this.me.id)
        .then((data) => (this.isfollows = data.result))
        .catch((err) => console.log(err.reponse.data));
    },
    enableEditing() {
      this.editing = true;
    },
    async update() {
      return UsersService.update(this.me)
        .then((result) => {
          this.$store.commit("auth/SET_USER", result);
        })
        .then(() => (this.editing = false))
        .catch((err) => {
          console.log(err.response.data);
        });
    },
    cancel() {
      this.editing = false;
    },
    clear() {
      // TODO does not work
      this.$refs.form.reset();
    },
    async follow() {
      return UsersService.follow(this.me.id)
        .then(() => this.loadFriendship())
        .catch((err) => console.log(err.reponse.data));
    },
    async unfollow() {
      return UsersService.unfollow(this.me.id)
        .then(() => this.loadFriendship())
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