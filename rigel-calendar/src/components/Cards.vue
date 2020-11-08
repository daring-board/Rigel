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
                            :color="color(item.my.status)"
                        >
                            <v-card-title 
                                class="headline"
                                style="white-space:pre-wrap; word-wrap:break-word;"
                            >{{item.display_name}}: {{btnWord(item.my)}}</v-card-title>
                            <v-divider></v-divider>
                            <v-card-text>
                                {{item.required}}<br/>
                                必要な接種回数：{{item.state}}<br/>
                                間隔日数：{{item.days}}<br/>
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </template>
            <!-- ダイアログコンテンツ -->
            <v-card class="deep-purple lighten-5">
                <Form/>
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
                if(vaccin.my.status == 'complete'){
                    console.log('No Chainge');
                }else if(vaccin.my.status == 'reservation'){
                    let personal = this.$store.state.personal;
                    personal.vaccins[vaccin.key].status = 'complete';
                    this.$store.commit('setPersonal', personal);

                    console.log(this.items[vaccin.id])
                    this.items[vaccin.id].my = personal.vaccins[vaccin.key];
                }else if(vaccin.my.status == 'nothing'){
                    let personal = this.$store.state.personal;
                    personal.vaccins[vaccin.key] = vaccin.my;
                    personal.vaccins[vaccin.key].status = 'reservation';
                    this.$store.commit('setPersonal', personal);

                    console.log(this.items[vaccin.id])
                    this.items[vaccin.id].my = personal.vaccins[vaccin.key];
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
                    vac.state = `${vac.needed} 回`;
                    vac.required = (vac.required)? '定期': '任意';
                    console.log(this.$store.state.personal)
                    if(k in this.$store.state.personal.vaccins){
                        vac.my = this.$store.state.personal.vaccins[k];
                    }else{
                        vac.my = {
                            'status': 'nothing',
                            'completed_num': 0, 'required': vac.state,
                            'reservation_date': ''
                        } 
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
            btnWord(vaccination){
                console.log(vaccination.status);
                let word = '未定義';
                if(vaccination.status == 'nothing'){
                    word = '未';
                }else if(vaccination.status == 'reservation'){
                    let date = vaccination.reservation_date.replace('-', '年');
                    date = date.replace('-', '月');
                    word = `予\r\n${date}日`;
                }else if(vaccination.status == 'complete'){
                    word = '完'
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
