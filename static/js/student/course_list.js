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
    },
    methods:{
         setCurrentDay:function(day){
              course_list.current_day=day;
         },

     }
})

 var course_list = new Vue({
     el: '#course-list',
     data:{
        times:["","08:00","09:45","13:30","15:20","17:05","19:20"],
        current_day:1,
        courses:new Array(7)
     },
    methods:{
         getColor:function(){
             var colors = ["rgba(242,113,28,0.72)","rgba(33,186,69,0.72)","rgba(33,133,208,0.72)","rgba(163,51,200,0.72)","rgba(224,57,151,0.72"];
             var index = parseInt(Math.random()*4);
             return colors[index];
         },
        jump:function(course_id){
             window.location.href= "/student/course_detail?open_id="+urlParam.open_id+"&course_id="+course_id;
        }
    }
})
$(function () {
    var week = (selected_week.selected_week);
    var time = new Date();
    course_list.current_day = time.getDay();
    week = week.replace(/[^0-9]/g,'');
    api.get('/api/u/course/list', {open_id: urlParam.open_id, week:parseInt(week)}, function (data) {
        course_list.courses = new Array(7);
        for(var i = 1; i < 8; i++){
            course_list.courses[i - 1] = new Array(6);
            for(var j = 1; j < 8; j++){
                course_list.courses[i-1][j-1] = new Array(2);
                course_list.courses[i-1][j-1][0] = "";
                course_list.courses[i-1][j-1][1] = "";
            }
        }
        for(var k = 0; k < data.length; k++){
            var course = data[k]["time"][1];
            var day = data[k]["time"][0];
            course_list.courses[day-1][course-1][0] = data[k]["name"];
            course_list.courses[day-1][course-1][1] = data[k]["course_id"];
            console.log( course_list.courses[day-1][course-1][1]);
        }
        successHolder.loading = false;
        successHolder.loaded = true;
    }, dftFail);
    $('#show-week').dropdown();
});