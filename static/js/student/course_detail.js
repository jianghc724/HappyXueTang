var successHolder = new Vue({
    el: '#successHolder',
    data: {
        loading:true,
        loaded:false
    }
})
var course_meta = new Vue({
    el:"#course-meta",
    data:{
        name:"",
        status:0,
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
             window.location.href= "/student/course_detail?open_id=urlParam.open_id&&course_id="+course_id;
        }
    }
})
$(function () {
    console.log(urlParam.course_id);
    api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id,status:0}, function (data) {
        course_meta.name = data["name"];
        course_meta.status = data["status"];
        successHolder.loading = false;
        successHolder.loaded = true;
    }, dftFail);
    $('#show-week').dropdown();
});