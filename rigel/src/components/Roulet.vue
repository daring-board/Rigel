<template>
  <div class="roulet">
    <div>メインメニュー名：{{menu}}</div>
    <div>サブメニュー名：{{sub}}</div>
    <b-button class="roulet-btn" @click="start">
		Roulet Start!
	</b-button>
  </div>
</template>

<script>

export default {
  name: 'Roulet',
  data: function(){
    return {
      menu: 'None',
      sub: 'None',
    }
  },
  methods: {
    start(){
      /* eslint-disable */
      console.log('クリックしました！')
      this.choiceMain()
      this.choiceSub()
    },
    choiceMain(){
      var menu_list = [
        'ハンバーグ', 'カレー', 'チャーハン', 'ムニエル', '焼き魚',
        'とんてき', 'ビフテキ', 'とんかつ', '唐揚げ', '鶏肉のサッパリ煮',
        '肉巻き', '肉詰め', 'おでん', '水炊き', 'キムチ鍋',
        '寄せ鍋', 'シチュー', 'ミルフィーユ鍋', 'すき焼き', '野菜炒め'
      ]
      var len = menu_list.length
      var prob = Math.random()
      this.menu = menu_list[Math.floor(prob * len)]
    },
    choiceSub(){
      var menu_list = [
        'フレッシュサラダ', 'ポテトサラダ', 'マカロニサラダ', 'なめろう', 'キャベツナ',
        '冷奴', '豚汁', '味噌汁', 'ポトフ', '酢の物',
        '和え物', '卵焼き', 'ゆで卵', 'ナムル', '中華スープ',
        'コンソメスープ'
      ]
      var len = menu_list.length
      var prob = Math.random()
      this.sub = menu_list[Math.floor(prob * len)]
    }
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
