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
      const res = await Promise.all([this.algorithm1()])
      /* eslint-disable */
      console.log(res)
      if(!res[0]){
        await this.algorithm2()
      }
        // await this.algorithm1()
    },
    reset: function(){
      // let data = [
      //   [0, 0, 0, 0, 0, 5, 0, 0, 0],
      //   [0, 0, 6, 1, 2, 7, 5, 4, 0],
      //   [0, 0, 4, 0, 0, 0, 2, 0, 0],
      //   [5, 1, 0, 4, 0, 6, 0, 0, 8],
      //   [0, 0, 0, 0, 0, 0, 0, 0, 0],
      //   [8, 0, 0, 9, 0, 1, 0, 6, 5],
      //   [0, 0, 5, 0, 0, 0, 6, 0, 0],
      //   [0, 2, 9, 6, 5, 8, 7, 0, 0],
      //   [0, 0, 0, 2, 0, 0, 0, 0, 0],
      // ]
      let data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
      ]
      this.items = []
      data.forEach(row => {
        let n_list = []
        row.forEach(el => {
          let obj = {
              'num': el,
              'candidates': [1, 2, 3, 4, 5, 6, 7, 8, 9],
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
    algorithm1: async function(){
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
      obj['candidates'] = []
      this.items[pos[0]].splice(pos[1], 1, obj)
      /* eslint-disable */
      console.log(pos, k)
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
    async algorithm2(){
      let counter = 0
      let num = 1

      while(counter < 30){
        const res = await this.checkLines(num)
        counter++

        let exclude_is_end = true
        if(this.isDone()){
          /* eslint-disable */
          console.log(counter)
          return
        }
        // next Number
        num++
        if(num == this.size+1 && res){
          let is_end = await this.checkCandidates()
          exclude_is_end = await this.excludeCandidates()
          console.log(is_end, exclude_is_end)
          num = 1
        }
      }
    },
    async checkLines(num){
      console.log('checkLines')
      for(let blk_idx=0;blk_idx<this.size;blk_idx++){
        let candidates = []
        let base_pos_x = blk_idx % 3 * 3
        let base_pos_y = Math.floor(blk_idx / 3) * 3
        let exclude_block_flag = false
        for(let i=base_pos_x;i<base_pos_x+3;i++){
          for(let j=base_pos_y;j<base_pos_y+3;j++){
            if((this.items[i][j]['num'] == num) && (this.items[i][j]['status'] == 'fixed')){
              exclude_block_flag = true
              break
            }
          }
        }
        if(exclude_block_flag){
          for(let i=base_pos_x;i<base_pos_x+3;i++){
            for(let j=base_pos_y;j<base_pos_y+3;j++){
              this.items[i][j]['candidates'] = this.items[i][j]['candidates'].filter(c => c != num)
            }
          }
          continue
        }
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

        exclude_row_lines.forEach(i => {
          for(let j=0;j<this.size;j++){
            this.items[i][j]['candidates'] = this.items[i][j]['candidates'].filter(c => c != num)
          }
        })

        exclude_col_lines.forEach(j => {
          for(let i=0;i<this.size;i++){
            this.items[i][j]['candidates'] = this.items[i][j]['candidates'].filter(c => c != num)
          }
        })

        let blk_pos = [
          [base_pos_x, base_pos_y], [base_pos_x, base_pos_y+1], [base_pos_x, base_pos_y+2],
          [base_pos_x+1, base_pos_y], [base_pos_x+1, base_pos_y+1], [base_pos_x+1, base_pos_y+2],
          [base_pos_x+2, base_pos_y], [base_pos_x+2, base_pos_y+1], [base_pos_x+2, base_pos_y+2],
        ]
        blk_pos.forEach(p => {
          if(this.items[p[0]][p[1]]['status'] == 'fixed'){
            return
          }
          if(!exclude_row_lines.includes(p[0]) && !exclude_col_lines.includes(p[1])){
            candidates.push(p)
            this.items[p[0]][p[1]]['candidates'].push(num)
            this.items[p[0]][p[1]]['candidates'] = this.items[p[0]][p[1]]['candidates'].filter(
              (elem, index, self) => self.indexOf(elem) === index
            )
          }
        })
        if(candidates.length == 1){
          this.setFixNumber(candidates[0], num)

          let pos = candidates[0]
          await this.excludeBlockCandidates(pos[0], pos[1], num)
          await this.excludeRowCandidates(pos[0], pos[1], num)
          await this.excludeColCandidates(pos[0], pos[1], num)
        }
      }
      return true
    },
    async checkCandidates(){
      console.log('checkCandidates')
      for(let i=0;i<this.size;i++){
        for(let j=0;j<this.size;j++){
          if(this.items[i][j]['status'] == 'fixed') continue
          console.log([i, j], this.items[i][j]['candidates'])
          if(this.items[i][j]['candidates'].length == 1){
            let num = this.items[i][j]['candidates'][0]
            this.setFixNumber([i, j], num)
            await this.excludeBlockCandidates(i, j, num)
            await this.excludeRowCandidates(i, j, num)
            await this.excludeColCandidates(i, j, num)
          }
        }
      }
      await this.checkCandidatesBlock()
      await this.checkCandidatesCol()
      // await this.checkCandidatesRow()
      return true
    },
    checkCandidatesCol(){
      for(let i=0;i<this.size;i++){
        let num_counter = [-1, 0,0,0, 0,0,0, 0,0,0]
        for(let j=0;j<this.size;j++){
          this.items[i][j]['candidates'].forEach(n => {
            num_counter[n]++
          })
        }

        num_counter.forEach(async (n, idx) => {
          if(n != 1) return
          for(let j=0;j<this.size;j++){
            if(this.items[i][j]['candidates'].includes(idx)){
              this.setFixNumber([i, j], idx)
              await this.excludeBlockCandidates(i, j, idx)
              await this.excludeRowCandidates(i, j, idx)
              break
            }
          }
        })
      }
    },
    checkCandidatesRow(){
      for(let j=0;j<this.size;j++){
        let num_counter = [-1, 0,0,0, 0,0,0, 0,0,0]
        for(let i=0;i<this.size;i++){
          this.items[i][j]['candidates'].forEach(n => {
            num_counter[n]++
          })
        }

        console.log(num_counter)
        num_counter.forEach(async (n, idx) => {
          if(n != 1) return
          for(let i=0;i<this.size;i++){
            if(this.items[i][j]['candidates'].includes(idx)){
              this.setFixNumber([i, j], idx)
              await this.excludeBlockCandidates(i, j, idx)
              await this.excludeColCandidates(i, j, idx)
              break
            }
          }
        })
      }
    },
    checkCandidatesBlock(){
      for(let blk_idx=0;blk_idx<this.size;blk_idx++){
        let base_pos_x = blk_idx % 3 * 3
        let base_pos_y = Math.floor(blk_idx / 3) * 3
        let num_counter = [-1, 0,0,0, 0,0,0, 0,0,0]
        for(let i=base_pos_x;i<base_pos_x+3;i++){
          for(let j=base_pos_y;j<base_pos_y+3;j++){
            this.items[i][j]['candidates'].forEach(n => {
              num_counter[n]++
            })
          }
        }

        num_counter.forEach((n, idx) => {
          if(n != 1) return
          for(let i=base_pos_x;i<base_pos_x+3;i++){
            for(let j=base_pos_y;j<base_pos_y+3;j++){
              if(this.items[i][j]['candidates'].includes(idx)){
                this.setFixNumber([i, j], idx)
                this.excludeColCandidates(i, j, idx)
                this.excludeRowCandidates(i, j, idx)
                break
              }
            }
          }
        })
      }
    },
    excludeColCandidates(i, j, n){
      for(i=0;i<this.size;i++){
        this.items[i][j]['candidates'] = this.items[i][j]['candidates'].filter(c => c != n)
      }
    },
    excludeRowCandidates(i, j, n){
      for(j=0;j<this.size;j++){
        this.items[i][j]['candidates'] = this.items[i][j]['candidates'].filter(c => c != n)
      }
    },
    excludeBlockCandidates(i, j, n){
      let base_pos_x = Math.floor(i / 3) * 3
      let base_pos_y = Math.floor(j / 3) * 3
      for(i=base_pos_x;i<base_pos_x+3;i++){
        for(j=base_pos_y;j<base_pos_y+3;j++){
          this.items[i][j]['candidates'] = this.items[i][j]['candidates'].filter(c => c != n)
        }
      }
    },
    uniqueAndOne(exclude_list, blk_idx){
      exclude_list[blk_idx] = exclude_list[blk_idx].filter(
        (elem, index, self) => self.indexOf(elem) === index
      )
      return exclude_list

    },
    async excludeCandidates(){
      console.log('excludeCandidates')
      await this.options.forEach(async n => {
        let exclude_col_lines = {}
        let exclude_row_lines = {}
        for(let blk_idx=0;blk_idx<this.size;blk_idx++){
          let base_pos_x = blk_idx % 3 * 3
          let base_pos_y = Math.floor(blk_idx / 3) * 3
          exclude_col_lines[blk_idx] = []
          exclude_row_lines[blk_idx] = []
          for(let i=base_pos_x;i<base_pos_x+3;i++){
            for(let j=base_pos_y;j<base_pos_y+3;j++){
              if(this.items[i][j]['candidates'].includes(n)){
                exclude_col_lines[blk_idx].push(j)
                exclude_row_lines[blk_idx].push(i)
              }
            }
          }
          exclude_col_lines = await this.uniqueAndOne(exclude_col_lines, blk_idx)
          exclude_row_lines = await this.uniqueAndOne(exclude_row_lines, blk_idx)
        }

        for(let blk_idx=0;blk_idx<this.size;blk_idx++){
          if(exclude_col_lines[blk_idx].length != 1){
            delete exclude_col_lines[blk_idx]
          }
          if(exclude_row_lines[blk_idx].length != 1){
            delete exclude_row_lines[blk_idx]
          }
        }

        // console.log('col', n, exclude_col_lines)
        for(let blk_idx in exclude_col_lines){
          let j = exclude_col_lines[blk_idx][0]
          for(let i=0;i<this.size;i++){
            let base_pos_x = blk_idx % 3 * 3
            if(i == base_pos_x) continue
            if(i == base_pos_x+1) continue
            if(i == base_pos_x+2) continue
            if(this.items[i][j]['status'] == 'fixed') continue
            // console.log(i, j, n)
            // console.log(this.items[i][j]['candidates'])
            this.items[i][j]['candidates'] = this.items[i][j]['candidates'].filter(c => c != n)
            // console.log(this.items[i][j]['candidates'])
          }
        }

        // console.log('row', n, exclude_row_lines)
        for(let blk_idx in exclude_row_lines){
          let i = exclude_row_lines[blk_idx][0]
          for(let j=0;j<this.size;j++){
            let base_pos_y = Math.floor(blk_idx / 3) * 3
            if(j == base_pos_y) continue
            if(j == base_pos_y+1) continue
            if(j == base_pos_y+2) continue
            if(this.items[i][j]['status'] == 'fixed') continue
            // console.log(i, j, n)
            // console.log(this.items[i][j]['candidates'])
            this.items[i][j]['candidates'] = this.items[i][j]['candidates'].filter(c => c != n)
            // console.log(this.items[i][j]['candidates'] )
          }
        }
      })
      return true
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
