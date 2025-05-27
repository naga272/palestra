<template>
  <div>
    <form @submit.prevent="getRegistrazione">
      <input type="text"      placeholder="username"  v-model="username"><br>
      <input type="text"      placeholder="nome"      v-model="nome"><br>
      <input type="text"      placeholder="cognome"   v-model="cognome"><br>
      <input type="password"  placeholder="password"  v-model="password"><br>
      <input type="eta"       placeholder="eta"       v-model="eta"><br>
      <input type="submit">
    </form>
  </div>
</template>


<script>

import axios from "axios";


function getCookie(name) 
{
  // funzione per ottenere il nome del token
  const value = '; ' + (document.cookie + ![]);
  const parts = value.split('; ' + name + '=');

  if (parts.length === 2)
    return parts.pop().split(';').shift()

}


export default {
  name: 'getLogin',
  mounted() {

    // richiesta per ottenere il token
    axios.get("http://127.0.0.1:8000/api/csrf/", {
      withcredentials : true 
    })
    .then(res => { 
      console.log("token ottenuto", res);
    })
    .catch(err => {
      console.log("token non ottenuto", err);
    })
  }, 
  methods : {
    getRegistrazione() {
      axios.post("http://127.0.0.1:8000/api/registrazione/", {
        username: this.username,
        password: this.password,
        nome:     this.nome,
        cognome:  this.cognome,
        eta:      this.eta,
      }, {
        headers : {
          'X_CSRFToken' : getCookie("csrftoken"),
          // withcredentials : true 
        }
      })
      .then(res => {
        console.log("answer da django: ", res.data);
      })
      .catch(err => {
        console.log("Errore", err);
      })
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
