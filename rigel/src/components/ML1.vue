<template>
  <div class="ml1">
    <video autoplay playsinline muted id="webcam" :width="width" :height="height"></video>
    <div v-if="!is_try">
      <b-button @click="start_process">賢くなるAIを試す</b-button>
    </div>
    <div v-else>
      <b-spinner v-if="is_loading" variant="primary" label="Spinning"></b-spinner>
      <div>{{message}}</div>

      <div>
        <p>下のボタンを押下するとAIが画像を覚えてくれます。</p>
        <p>『Aの画像はこれだよ』という気持ちでボタンをクリックしてください。</p>
        <p>AIは画像を3種類だけ覚える事ができます。（A, B, Cの3種類）</p>
      </div>
      <b-button class='button' @click="addExample(0)">Add A</b-button>
      <b-button class='button' @click="addExample(1)">Add B</b-button>
      <b-button class='button' @click="addExample(2)">Add C</b-button>
    </div>
  </div>
</template>

<script>
import * as tf from '@tensorflow/tfjs'
import * as mobilenet from '@tensorflow-models/mobilenet'
import * as knn from '@tensorflow-models/knn-classifier'

export default {
  name: 'ML1',
  data: function(){
    return {
      is_loading: false,
      is_try: false,
      net: null,
      classifier: null,
      message: '',
      webcam: null,
      width: 0,
      height: 0
    }
  },
  methods: {
    addExample: async function(classId){
      const img = await this.webcam.capture()
      const activation = this.net.infer(img, 'conv_preds')
      this.classifier.addExample(activation, classId)
      img.dispose()
    },
    start_process: function(){
      this.is_try = true
      this.processing()
    },
    processing: async function(){
      /* eslint-disable */
      this.is_loading = true

      console.log('Loading mobilenet..')
      this.net = await mobilenet.load()
      console.log('Successfully loaded model')

      console.log('Create Classifier')
      this.classifier = knn.create()
      console.log('Successfully created classifier')
      this.is_loading = false

      this.width = 224
      this.height = 224
      const webcamEl = document.getElementById('webcam')
      this.webcam = await tf.data.webcam(webcamEl)
      
      while (true) {
        if (this.classifier.getNumClasses() > 0) {
          const img = await this.webcam.capture()
          const activation = this.net.infer(img, 'conv_preds')
          console.log(activation)
          const result = await this.classifier.predictClass(activation);
          const classes = ['A', 'B', 'C']
          var pre = ''
          var post = ''
          if(result.confidences[result.label] > 0.9){
            pre = ''
          }else if(result.confidences[result.label] > 0.6){
            pre = 'たぶん、'
          }else if(result.confidences[result.label] > 0.3){
            pre = 'もしかして、'
            post = '?'
          }else{
            continue
          }
          this.message = `${pre}${classes[result.label]}が見えている${post}\n`
          img.dispose();
        }
        await tf.nextFrame();
      }
    }
  }
}
</script>
<style scoped>
.button {
  margin: 10px;
}
</style>>
