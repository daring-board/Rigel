<template>
  <div class="number-place">
    <div v-if="!is_try">
      <b-button class="np-btn" @click="start_process">数独（NumberPlace）</b-button>
    </div>
    <div v-else>
      <b-container>
        <b-row class='row-centering'>
          <b-container class="np-container" style="margin-top: 10px">
            <b-row :class="is_single_line_row(r_idx)" v-for="(row, r_idx) in items" :key="r_idx">
              <b-col :class="is_single_line_col(c_idx)" v-for="(col, c_idx) in row" :key="c_idx">
                <b-button variant="link" @click="select_position(r_idx, c_idx)">{{col.num}}</b-button>
              </b-col>
            </b-row>
          </b-container>
        </b-row>
        <b-row style="margin-top: 10px">
          <b-col style="padding: 0px" v-for="(num, index) in options" :key="index">
            <b-button
              variant="outline-primary" style="border: solid;"
              @click="select(num)"
            >{{num}}</b-button>
          </b-col>
        </b-row>
        <b-row class='row-centering' style="margin-top: 10px">
          <b-col>
            <b-button variant="primary" @click="solve">解く</b-button>
          </b-col>
          <b-col>
            <b-button variant="primary" @click="reset">再入力</b-button>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NumberPlace',
  data: function(){
    return {
      is_try: false,
      items: [],
      options: [1, 2, 3, 4, 5, 6, 7, 8, 9],
      position: [0, 0],
      size: 9,
      end_of_loop: 500,
    }
  },
  mounted: function() {
    this.reset()
  },
  methods: {
    start_process: function(){
      this.is_try = true
    },
    solve: async function() {
      if(await this.algorithm1()){
        return
      }else{
        await this.algorithm2()
        await this.algorithm1()
      }
    },
    reset: function(){
      let data = [
        [0, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 6, 1, 2, 7, 5, 4, 0],
        [0, 0, 4, 0, 0, 0, 2, 0, 0],
        [5, 1, 0, 4, 0, 6, 0, 0, 8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 9, 0, 1, 0, 6, 5],
        [0, 0, 5, 0, 0, 0, 6, 0, 0],
        [0, 2, 9, 6, 5, 8, 7, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, 0],
      ]
      // let data = [
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      // ]
      this.items = []
      data.forEach(row => {
        let n_list = []
        row.forEach(el => {
          let obj = {
              'num': el,
              'candidates': this.options,
              'status': 'free'
          }
          if (el != 0){
            obj['status'] = 'fixed'
            obj['candidates'] = []
          }
          n_list.push(obj)
        });
        this.items.push(n_list)
      });
    },
    select: function(num){
      let obj = {
        'num': num, 'candidates': [],
        'status': 'fixed'
      }
      this.items[this.position[0]].splice(this.position[1], 1, obj)
    },
    select_position: function(r_idx, c_idx){
      this.position = [r_idx, c_idx]
    },
    is_single_line_row: function(r_idx){
      if (r_idx != 0 && r_idx != 8 && r_idx % 3 == 2){
        return "np-row-single"
      }else{
        return "np-row"
      }
    },
    is_single_line_col: function(c_idx){
      if (c_idx != 0 && c_idx != 8 && c_idx % 3 == 0){
        return "np-col-single"
      }else{
        return "np-col"
      }
    },
    validation_input: function(){

    },
    algorithm1: function(){
      let pos = [0, 0]
      let counter = 0

      while(counter < this.end_of_loop){
        this.search(pos)
        counter++

        if(this.isDone()){
          /* eslint-disable */
          console.log(counter)
          return true
        }
        pos = this.nextPosition(pos)
      }
      return false
    },
    search(pos) {
      if(this.items[pos[0]][[pos[1]]]['status'] != 'free') return
      let candidates = []
      for(let k=1;k<=this.size;k++){
        if(this.rowCheck(pos, k)) continue
        if(this.colCheck(pos, k)) continue
        if(this.blockCheck(pos, k)) continue
        candidates.push(k)
      }
      if(candidates.length == 1){
        let k = candidates[0]
        this.setFixNumber(pos, k)
        /* eslint-disable */
        console.log(pos, k)
      }
    },
    isDone(){
      for(let i=0;i<this.size;i++){
        for(let j=0;j<this.size;j++){
          if(this.items[i][j]['status'] != 'fixed'){
            return false
          }
        }
      }
      return true
    },
    setFixNumber(pos, k){
      let obj = this.items[pos[0]][pos[1]]
      obj['num'] = k
      obj['status'] = 'fixed'
      this.items[pos[0]].splice(pos[1], 1, obj)
    },
    rowCheck(pos, k){
      let is_find_row = false
      for(let row=0;row<this.size;row++){
        if(this.items[row][pos[1]]['num'] == k){
          is_find_row = true
          break
        }
      }
      return is_find_row
    },
    colCheck(pos, k){
      let is_find_col = false
      for(let col=0;col<this.size;col++){
        if(this.items[pos[0]][col]['num'] == k){
          is_find_col = true
          break
        }
      }
      return is_find_col
    },
    blockCheck(pos, k){
      const row_start = Math.floor(pos[0] / 3) * 3
      const row_end = Math.floor(pos[0] / 3) * 3 + 2
      const col_start = Math.floor(pos[1] / 3) * 3
      const col_end = Math.floor(pos[1] / 3) * 3 + 2
      let is_find_block = false
      for(let row=row_start;row<=row_end;row++){
        for(let col=col_start;col<=col_end;col++){
          if(this.items[row][col]['num'] == k){
            is_find_block = true
            break
          }
        }
      }
      return is_find_block
    },
    nextPosition(pos){
      let ret = [pos[0], pos[1]+1]
      if(ret[1] == this.size){
        ret = [ret[0]+1, 0]
      }
      if(ret[0] == this.size){
        ret = [0, ret[1]]
      }
      return ret
    },
    algorithm2(){
      let counter = 0
      let num = 1

      while(counter < this.end_of_loop){
        this.checkLines(num)
        counter++

        if(this.isDone()){
          /* eslint-disable */
          console.log(counter)
          return
        }
        // next Number
        num++
        if(num == this.size+1) num = 1
      }
    },
    checkLines(num){
      let exclude_row_lines = []
      let exclude_col_lines = []

      for(let i=0;i<this.size;i++){
        for(let j=0;j<this.size;j++){
          if(this.items[i][j]['num'] == num){
            exclude_row_lines.push(i)
            exclude_col_lines.push(j)
          }
        }
      }

      let candidates = []
      for(let blk_idx=0;blk_idx<this.size;blk_idx++){
        let base_pos = blk_idx*3
        let blk_pos = [
          [base_pos, base_pos], [base_pos, base_pos+1], [base_pos, base_pos+2],
          [base_pos+1, base_pos], [base_pos+1, base_pos+1], [base_pos+1, base_pos+2],
          [base_pos+2, base_pos], [base_pos+2, base_pos+1], [base_pos+2, base_pos+2],
        ]
        blk_pos.forEach(p => {
          if(!exclude_row_lines.includes(p[0]) && !exclude_col_lines.includes(p[1])){
            candidates.push(p)
          }
        })
        if(candidates.length == 1){
          this.setFixNumber(candidates[0], num)
          /* eslint-disable */
          console.log(candidates[0], num)
        }
      }
    }
  }
}
</script>
<style scoped>
.np-btn {
  margin-top: 35px;
}
.row-centering {
  margin: 0 auto;
}
.np-col {
  border-left: 2px solid #333;
  font-size: 100%;
  padding: 0px;
}
.np-col-single {
  border-left: 4px dashed black;
  font-size: 100%;
  padding: 0px;
}
.np-row {
  border-bottom: 2px solid #333;
  font-size: 100%;
  padding: 0px;
}
.np-row-single {
  border-bottom: 4px dashed black;
  font-size: 100%;
  padding: 0px;
}
.np-container {
  border-top: 2px solid #333;
  border-right: 2px solid #333;
  font-size: 100%;
}
</style>>
