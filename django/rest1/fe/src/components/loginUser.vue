

<template>

  <form @submit.prevent="inviaForm">
    <input type="text"      v-model="username" placeholder="username"><br>
    <input type="password"  v-model="password" placeholder="password"><br>
    <input type="submit">
  </form>
  
</template>

<script>


import axios from 'axios';


function getCookie(name) 
{
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


export default {
  mounted(){
    axios.get("http://localhost:8000/csrf/", {
      withCredentials: true
    }).then(() => {
      console.log("CSRF token ricevuto");
    })
  },
  methods: {
    inviaForm() {
      axios.post('http://localhost:8000/login/', {
        username: this.username,
        password: this.password
      },{
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
        },
        withCredentials: true
      })
      .then(res => {
        console.log(res.data["message"]);
      })
      .catch(err => {
        console.error("Errore:", err)
      });
    }
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
