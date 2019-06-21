<template>
  <div class="labeler">
    <img id="image" src="http://localhost:8080/c6b1effb02f050e72507eba2d5f8a2ff.jpg" width=224 height=224>
    <button @click="labeling">Labeling!!</button>
  </div>
</template>

<script>
import * as tf from '@tensorflow/tfjs'

export default {
  name: 'Labeling',
  props: {
    msg: String
  },
  data: function(){
    return {
      model: null
    }
  },
  mounted: function(){
    this.loadModel()
  },
  methods: {
    loadModel: function(){
      tf.loadLayersModel('http://localhost:8080/model/model.json').then(response => {
        this.model = response
      })
    },
    labeling(){
      /* eslint-disable */
      console.log(this.model)
      const img =  tf.browser.fromPixels(document.getElementById('image')).expandDims().div(tf.scalar(255))
      console.log(this.model.predict(img).data())
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
