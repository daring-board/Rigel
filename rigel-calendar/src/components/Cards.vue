<template>
    <v-container>
        <v-dialog v-model="dialog">
            <!-- アクティベータースロット -->
            <template v-slot:activator="{ on }">
                <v-row v-for="(item, key) in items" :key="key">
                    <v-col v-on="on" @click="selectVaccin(item)">
                        <v-card
                            max-width="500"
                            class="mx-auto text_default--text"
                            :color="color(item.status)"
                        >
                            <v-card-title class="headline">{{item.display_name}}: {{btnWord(item.status)}}</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text>
                                {{item.required}}<br/>
                                接種状況：{{item.state}}<br/>
                                間隔日数：{{item.days}}<br/>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </template>
            <!-- ダイアログコンテンツ -->
            <v-card class="deep-purple lighten-5">
                <v-card-text>
                    <Form/>
                </v-card-text>
                <v-card-actions>
                    <v-btn color="primary" @click="commit()">確定</v-btn>
                    <v-btn color="warning" @click="dialog = false">戻る</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
    import Form from '@/components/Form';

    export default {
        name: 'Cards',
        components: {Form},
        data: () => ({
            items: [],
            dialog: false
        }),
        props: ['month'],
        methods: {
            commit(){
                this.dialog = false;
                let vaccin = this.$store.state.selected;
                if(vaccin.status == 'complete'){
                    console.log('No Chainge');
                }else if(vaccin.status == 'reservation'){
                    let personal = this.$store.state.personal;
                    personal.status[vaccin.key] = 'complete';
                    this.$store.commit('setPersonal', personal);

                    console.log(this.items[vaccin.id])
                    this.items[vaccin.id].status = personal.status[vaccin.key];
                }else if(vaccin.status == 'nothing'){
                    let personal = this.$store.state.personal;
                    personal.status[vaccin.key] = 'reservation';
                    this.$store.commit('setPersonal', personal);

                    console.log(this.items[vaccin.id])
                    this.items[vaccin.id].status = personal.status[vaccin.key];
                }
            },
            selectVaccin(item){
                this.$store.commit('setSelect', item)
            },
            setItems(vaccinations) {
                const keys = Object.keys(vaccinations);
                console.log(keys);
                keys.forEach(k => {
                    let vac = vaccinations[k];
                    let month = parseInt(this.month)+1;
                    if(vac.spans.indexOf(month) < 0){
                        return
                    }
                    if(vac.recommends.indexOf(month) < 0){
                        return
                    }
                    let interval = `${vac.interval.num} ${vac.interval.unit}`;
                    vac.days = interval;
                    vac.state = `0 / ${vac.needed} 回`;
                    vac.required = (vac.required)? '定期': '任意';
                    console.log(this.$store.state.personal)
                    if(k in this.$store.state.personal.status){
                        vac.status = this.$store.state.personal.status[k];
                    }else{
                        vac.status = 'nothing'
                    }
                    vac.key = k;
                    vac.id = this.items.length;
                    this.items.push(vac);
                });
            },
            color(status){
                let color = 'white';
                if(status == 'nothing'){
                    color = 'warning';
                }else if(status == 'reservation'){
                    color = 'accent';
                }else if(status == 'complete'){
                    color = 'success'
                }
                return color;
            },
            btnWord(status){
                let word = '未定義';
                if(status == 'nothing'){
                    word = '未定';
                }else if(status == 'reservation'){
                    word = '予約済み(○月×日)';
                }else if(status == 'complete'){
                    word = '完了'
                }
                return word;
            }
        },
        watch:  {
            month: {
                handler: function(){
                    this.items = [];
                    console.log(this.month)
                    const vaccinations = this.$store.state.vaccinations;
                    console.log(JSON.stringify(vaccinations));
                    if(vaccinations == null){
                        this.$store.commit('getPersonal').then(() => {
                            this.setItems(vaccinations);
                            console.log(this.items);
                        });
                    }else{
                        this.setItems(vaccinations);
                        console.log(this.items);
                    }
                },
                immediate: true
            }
        }
    }
</script>
