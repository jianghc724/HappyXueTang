var successHolder = new Vue({
        el: '#successHolder',
        data: {
            loading:true,
            loaded:false
        }
    })
new Vue({
    el:'#week-menu'
})
var selected_week = new Vue({
    el: '#selected-week',
    data: {
        selected_week:"第0周"
    }
})
var day_list = new Vue({
    el: '#day-list',
    data:{
        week:[
            {
                text: '周一',
                id:"1"
            },
            {
                text: '周二',
                id:"2"
            },
            {
                text: '周三',
                id:"3"
            },
            {
                text: '周四',
                id:"4"
            },
            {
                text: '周五',
                id:"5"
            },
            {
                text: '周六',
                id:"6"
            },
            {
                text: '周日',
                id:"7"
            }
        ],
        transation_name_index:0,
        transation_names:["not-selected","selected"]
    },
    methods:{
         setCurrentDay:function(day){
              course_list.current_day=day;
              this.transation_name_index = (this.transation_name_index + 1) % 2;
         }
     }
})

 var course_list = new Vue({
     el: '#course-list',
     data:{
        times:["","08:00","09:45","13:30","15:15","19:20"],
        current_day:1,
        courses:[]
     }
})
$(function () {
    var week = (selected_week.selected_week);
    var time = new Date();
    course_list.current_day = time.getDay();
    week = week.replace(/[^0-9]/g,'');
    console.log(23333);
    api.get('/api/u/course/list', {open_id: urlParam.open_id, week:parseInt(week)}, function (data) {

        course_list.courses = new Array(7);
        for(var i = 1; i < 8; i++){
            course_list.courses[i - 1] = new Array();
        }
        successHolder.loading = false;
        successHolder.loaded = true;
    }, dftFail);
    $('#show-week').dropdown();
});