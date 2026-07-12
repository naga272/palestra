<template>
  <div>
    Hello World
  </div>
</template>

<script>
import axios from "axios"  


export default {
  name: 'HelloWorld',
  mounted() {
    axios.get("http://localhost:8000/api/hello", {
      withcredentials: true
    })
    .then(res => {
      console.log(res.data);
    })
  }
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
