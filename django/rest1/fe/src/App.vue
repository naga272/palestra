

<template>
  <div id="test">
    <loginUser v-for="i in count" :key="i"/>
    <button @click="foo">press me</button>
  </div>
</template>


<script>

import loginUser from './components/loginUser.vue'

export default {
  name: 'App',
  components: {
    loginUser
  },
  data() {
    return {
      count: 1
    }
  },
  methods: {
    foo() {
      this.count++;
    }
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
