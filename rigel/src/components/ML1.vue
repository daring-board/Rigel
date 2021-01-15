<template>
  <div class="ml1">
    <video autoplay playsinline muted id="webcam" :width="width" :height="height"></video>
    <div v-if="!is_try">
      <b-button class="ai-btn" @click="start_process">賢くなるAIを試す</b-button>
    </div>
    <div v-else>
      <b-spinner v-if="is_loading" variant="primary" label="Spinning"></b-spinner>
      <div>{{message}}</div>

      <div>
        <p>下のボタンを押下するとAIが画像を覚えてくれます。</p>
        <p>『class 1の画像はこれだよ』という気持ちでボタンを押してください。</p>
      </div>
      <b-container>
        <b-row class='row-centering'>
          <div v-for="(cls, key) in class_list" :key="key">
            <b-col>
              <b-button class='button' @click="addExample(key)">{{cls.class_name}}</b-button>
            </b-col>
          </div>
        </b-row>
        <b-row class='row-centering'>
          <b-button class='button' v-b-modal.add-modal>分類を増やす</b-button>
          <b-modal id="add-modal" title="分類を増やす" @ok='addClass()'>
            <b-row>
              <b-col><label>クラス名:</label></b-col>
              <b-col><b-form-input v-model="add_obj"></b-form-input></b-col>
            </b-row>
          </b-modal>
          <b-button class='button' v-b-modal.modify-modal>クラス名を変更</b-button>
          <b-modal id="modify-modal" title="クラス名を変更" hide-footer>
            <div v-for="(cls, key) in class_list" :key="key">
              <b-row>
                <b-col><label>クラス{{key+1}}の名称を変更:</label></b-col>
                <b-col><b-form-input v-model="cls.class_name"></b-form-input></b-col>
              </b-row>
            </div>
          </b-modal>
        </b-row>
        <b-row class='row-centering'>
          <b-button class='button' @click="saveKNN">学習したAIを保存</b-button>
          <b-button class='button' @click="loadKNN">学習済みAIを読込</b-button>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
import * as tf from '@tensorflow/tfjs'
import * as knn from '@tensorflow-models/knn-classifier'
import firebase from 'firebase/app'
import 'firebase/storage'
import axios from 'axios'

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
      height: 0,
      class_list: [
        {class_name: 'class 1'},
        {class_name: 'class 2'},
        {class_name: 'class 3'}
      ],
      add_obj: '',
      storageRef: ''
    }
  },
  mounted: function() {
    this.storageRef = firebase.storage().ref().child('ml1/knn.json')
  },
  methods: {
    saveKNN: async function() {
      /* eslint-disable */
      let dataset = this.classifier.getClassifierDataset()
      console.log(dataset)
      var datasetObj = {}
      Object.keys(dataset).forEach((key) => {
        let data = dataset[key].dataSync()
        datasetObj[key] = Array.from(data)
      });
      let jsonStr = JSON.stringify(datasetObj)
      console.log(jsonStr)
      localStorage.setItem("knn_classifier", jsonStr)
      let url = 'https://us-central1-rigel-b11c1.cloudfunctions.net/upload-knn'
      axios.post(url, {'JsonString': jsonStr}, {headers: {'Access-Control-Allow-Origin': '*'}})
        .then(response => {})
    },
    loadKNN: function(){
      /* eslint-disable */
      let dataset = localStorage.getItem("knn_classifier")
      let url = 'https://us-central1-rigel-b11c1.cloudfunctions.net/get-knn'
      axios.get(url, {headers: {'Access-Control-Allow-Origin': '*'}})
        .then(response => {
          var obj = JSON.parse(response.data)
          this.classifier = knn.create()
          Object.keys(obj).forEach((key) => {
            if (!Array.isArray(obj[key])) return
            obj[key] = tf.tensor(obj[key], [obj[key].length / 1280, 1280])
          }, obj)
          this.classifier.setClassifierDataset(obj)
        })
     },
    addClass: function(){
      if (this.add_obj.length === 0){
        this.class_list.push({class_name: 'class ' + (this.class_list.length+1)})
      }else{
        this.class_list.push({class_name: this.add_obj})
      }
    },
    addExample: async function(classId){
      const img = await this.webcam.capture()
      const y = tf.tensor1d(tf.tidy(() => {
        console.log(img)
        const x = tf.image
                  .resizeBilinear(img, [192, 192])
                  .toFloat()
                  .div(tf.scalar(255))
                  .expandDims()
        return this.net.predict(x).dataSync()
      }))
      this.classifier.addExample(y, classId)
      y.dispose()
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
      this.net = await tf.loadGraphModel(
        "https://tfhub.dev/google/tfjs-model/imagenet/mobilenet_v2_035_192/feature_vector/2/default/1",
        { fromTFHub: true }
      )
      console.log('Successfully loaded model')
      console.log(this.net)

      console.log('Create Classifier')
      this.classifier = knn.create()
      console.log('Successfully created classifier')
      this.is_loading = false

      const webcamEl = document.getElementById('webcam')
      this.webcam = await tf.data.webcam(webcamEl)

      while (true) {
        if (this.classifier.getNumClasses() > 0) {
          const img = await this.webcam.capture()
          const y = tf.tensor1d(tf.tidy(() => {
            const x = tf.image
                      .resizeBilinear(img, [192, 192])
                      .toFloat()
                      .div(tf.scalar(255))
                      .expandDims()
            return this.net.predict(x).dataSync()
          }))
          const result = await this.classifier.predictClass(y)
          y.dispose()
          img.dispose()
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
          this.message = `${pre}${this.class_list[result.label].class_name}が見えている${post}\n`
          result.dispose
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
.row-centering {
  margin: 0 auto;
}
</style>>
