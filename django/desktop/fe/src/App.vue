<template>
  <div id="container">
    <formLogin v-if="!isLoggedIn" @login-success="handleLoginSuccess" />
    <guiInit v-else :username="username" :filesystem="filesystem"/>
  </div>
</template>

<script>

import formLogin from './components/formDesktop.vue'
import guiInit from "./components/guiInit.vue"


export default {
  name: 'App',
  components: {
    formLogin,
    guiInit
  },
  data() {
    return {
      isLoggedIn: false,
      username: '',
      filesystem: {}
    }
  },
  methods: {
    handleLoginSuccess(data) {
      this.username = data.username;
      this.filesystem = data.filesystem;
      this.isLoggedIn = true;
    }
  }
}
</script>


<style>

  *{
    margin:0;
    padding:0;
    outline:none;
  }


  #container{
    width: 100%;
    height: 100vh;
    background-image: url("./assets/schermata_di_blocco_win11.jpg");
    background-position: relative;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    display: grid;
    place-items: center;
    z-index: 1;
  }

</style>
