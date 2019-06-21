<template>
  <div class="labeler">
    <img id="image" src="c6b1effb02f050e72507eba2d5f8a2ff.jpg" width=224 height=224>
    <button @click="labeling">Labeling!!</button>
    <p>{{estimate}}</p>
  </div>
</template>

<script>
import * as tf from '@tensorflow/tfjs'
import Labels from '../assets/labels.json'

export default {
  name: 'Labeling',
  data: function(){
    return {
      model: null,
      scores: null,
      labels: Labels,
      estimate: null,
    }
  },
  mounted: function(){
    this.loadModel()
  },
  methods: {
    loadModel(){
      tf.loadLayersModel('model/model.json').then(response => {
        this.model = response
      })
    },
    async labeling(){
      /* eslint-disable */
      console.log(this.model)
      const img =  tf.browser.fromPixels(document.getElementById('image')).expandDims().div(tf.scalar(255))
      this.scores = await this.model.predict(img).data()
      console.log(this.labels)
      this.estimate = this.labels[this.scores.indexOf(Math.max.apply(null, this.scores))]
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
