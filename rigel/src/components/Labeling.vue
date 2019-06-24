<template>
  <div class="labeler">
    <b-alert :show="model == null">モデルファイルをダウンロードしています。</b-alert>
    <b-container fluid>
      <b-row>
        <b-col>
          <b-card header="Step1 画像選択">
            <label class="file-upload">
              ラベリングする画像を選択
              <input type="file" @change="onFileChange"/>
            </label>
          </b-card>
        </b-col>
        <b-col>
          <b-card header="Step2 画像確認">
            <img id="image" :src="img" width="224" height="224">
          </b-card>
        </b-col>
        <b-col>
          <b-card header="Step3 判定する">
            <div v-if="!estimate">
              <b-spinner label="Spinning"></b-spinner>
            </div>
            <div v-else>
              <b-table dark :fields="fields" :items="estimate">
                <template slot="No" slot-scope="data">
                  {{ data.index + 1 }}
                </template>

                <template slot="score" slot-scope="data">
                  {{ (data.item.score * 100).toFixed(2) }} %
                </template>
              </b-table>
            </div>
            <button @click="labeling">Labeling!!</button>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
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
      img: 'logo.png',
      processing: false,
      fields: [
        'No',
        {'key': 'label', 'label': 'ラベル'},
        {'key':'score', 'label': '確信度'}
      ]
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
      this.estimate = null
      /* eslint-disable */
      console.log(this.model)
      const img =  tf.browser.fromPixels(document.getElementById('image')).expandDims().div(tf.scalar(255))
      this.scores = await this.model.predict(img).data()

      let score_list = []
      this.scores.forEach(function(value, index){
        score_list.push({'label': Labels[index], 'score': value})
      })

      score_list.sort(function(a,b){
        if(a.score < b.score) return 1
        if(a.score > b.score) return -1
        return 0
      })

      this.estimate = score_list.slice(0, 5)
    },
    onFileChange(event) {
      const files = event.target.files || event.dataTransfer.files
      const reader = new FileReader();
      reader.onload = e => {
        this.img = e.target.result;
      }
      reader.readAsDataURL(files[0]);
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
label > input {
  display: none;
}

label {
  padding: 0 1rem;
  border: solid 1px #555;
  background-color: aqua;
} 
</style>
