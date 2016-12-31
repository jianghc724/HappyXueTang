var successHolder = new Vue({
    el: '#successHolder',
    data: {
        loading:true,
    }
})
var course_meta = new Vue({
    el:"#course-meta",
    data:{
        name:"",
        status:0,
        teacher:"",
        email:"",
        ratings:[],
        rating_texts:["课堂氛围：","课程收获：", "课程负担："],
        notices:[],
        homeworks:[],
        files:[]
    },
    methods:{
        getNotice:function(){
            this.status = 1;
            api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id, status:1}, function (data) {
                console.log(data);
                course_meta.notices = data["notice_detail"];
            }, dftFail);
        },
        getHomework:function(){
            this.status = 2;
            api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id,status:2}, function (data) {
                course_meta.homeworks = data["new_oprations"];
            }, dftFail);
        },
        lastTime:function(publish, current){
            var last_time = (current.getTime() - publish.getTime())/1000;
            var last_day = Math.floor(last_time/86400);
            var last_hour = Math.floor(last_time%86400/3600);
            var last_minute = Math.floor(last_time%86400%3600/60);
            var return_str = "";
            if(last_day != 0)
                return_str += last_day + "天";
            if(last_hour != 0)
                return_str += last_hour + "小时";
            if(last_minute != 0)
                return_str += last_minute + "分钟";
            if(last_day == 0 && last_hour == 0 && last_minute == 0)
                return_str += "刚刚发布。"
            else
                return_str += "前发布。" 
        },
    }
})

$(function () {
    console.log(urlParam.course_id);
    api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id,status:0}, function (data) {
        course_meta.name = data["name"];
        course_meta.status = data["status"];
        course_meta.teacher = data["teacher"];
        course_meta.email = data["email"];
        course_meta.ratings = data["ratings"];
        for(var i = 0; i < 3; i++){
            course_meta.ratings[i] = Math.round(course_meta.ratings[i]);
            if(course_meta.ratings[i] < 0)
                course_meta.ratings[i] = 0;
        }
        successHolder.loading = false;
    }, dftFail);
    $('#show-week').dropdown();
});