<template>
  <div id="login_form_container">
    <form @submit.prevent="LoginForm">
      <div id="orarioForm"></div>
      <input v-model="username" required placeholder="username" type="text" id="id_username">
      <input v-model="password" required placeholder="username" type="password" id="id_password">
      <input type="submit" value="login" id="submit_login">
    </form>
  </div>
</template>

<script>

import axios from "axios";


function getCookie(name)
{
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)')); 
  return match;
}


export default {
  name: 'formLogin',
  mounted() {
    axios.get("http://127.0.0.1:8000/api/get_token", {withCredentials: true});

    const orario = document.getElementById("orarioForm");

    const getOrario = () => {
      const ora = new Date();
      const opzioni = {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false
      };

      const orarioFormattato = ora.toLocaleTimeString("it-IT", opzioni);
      orario.innerHTML = orarioFormattato;
    }

    setInterval(getOrario, 1000);
    getOrario();
  },
  methods: {
    LoginForm() {
      axios.post("http://127.0.0.1:8000/api/login", {
          username: this.username,
          password: this.password
        }, {
          headers: {
            "X-CSRFToken" : getCookie("csrftoken"),
          },
        }, {
          withCredentials: true
        }
      )
      .then(res => {
        // console.log(res);
        if (res.data.success === true) {
          this.$emit('login-success', {
            username: this.username,
            filesystem: res.data.filesystem
          });
        }
      })
      .catch(err => {
        console.log(err.response.data);
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  #login_form_container{
    margin: 0 auto;
  }

  #orarioForm{
    text-align: center;
    font-size: 3em;
    color:#fff;
  }

  #id_username, #id_password, #submit_login{
    font-size: 1.2em;
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
    text-align: center;
    border-radius: 5px;
    background-color: #1e1e1e;
    color: #fff;
    border-top: 2px solid rgb(156, 156, 156);
    border-bottom: 2px solid rgb(168, 44, 44);
    border-right: 2px solid rgb(156, 156, 156);
    border-left: 2px solid rgb(156, 156, 156);
    margin-bottom: 10px;
    transition: all .7s ease;
  }


  #id_username:hover, #id_password:hover, #submit_login:hover{
    border-top: 2px solid grey;
    border-bottom: 2px solid red;
    border-right: 2px solid grey;
    border-left: 2px solid grey;
  }


  #id_username:focus, #id_password:focus {
    background-color: #fff;
    color: #1e1e1e;
    border-top: 2px solid grey;
    border-bottom: 2px solid red;
    border-right: 2px solid grey;
    border-left: 2px solid grey;
  }


  #submit_login:hover{
    cursor: pointer;
  }
</style>
