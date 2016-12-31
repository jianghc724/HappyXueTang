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
        remain:[],
        files:[],
    },
    methods:{
        getNotice:function(){
            this.status = 1;
            api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id, status:1}, function (data) {
                course_meta.notices = data["notice_detail"];
            }, dftFail);
        },
        getHomework:function(){
            this.status = 2;
            api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id,status:2}, function (data) {
                this.homeworks = data["new_operations"];
                for(var i = 0; i < this.homeworks.length;i++){
                    var remain_array = getRemainTime(this.homeworks.duedate, this.homeworks.current_time);
                    remain.append(remain_array);
                }
            }, dftFail);
        },
        getTime:function(time){
            var date = new Date(time).toJSON();
            var date_array = date.split('T');
            var time_array = (date_array[1].split('.'))[0].split(':');
            return_time = date_array[0] + " " + time_array[0] + ":" + time_array[1] + ":"+ time_array[2];
            return return_time;
        },
        getRemainTime:function(due, current){
            var current_date = new Date(current*1000);
            var due_date = new Date(due);
            var time = (due_date.getTime() - current_date.getTime())/1000;
            var day = Math.floor(time/86400);
            var hour = Math.floor(time%86400/3600);
            var minute = Math.floor(time%86400%3600/60);
            return [day, hour, minute];
        },
    }
})

$(function () {
    api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id,status:0}, function (data) {
        course_meta.name = data["name"];
        course_meta.status = data["status"];
        course_meta.teacher = data["teacher"];
        course_meta.email = data["email"];
        api.get('/api/u/course/comments/overview', {open_id: urlParam.open_id, course_id:urlParam.course_id}, function (data) {
            course_meta.ratings = data["ratings"];
            for(var i = 0; i < 3; i++){
                course_meta.ratings[i] = Math.round(course_meta.ratings[i]);
                if(course_meta.ratings[i] < 0)
                    course_meta.ratings[i] = 0;
            }
        }, dftFail);
        successHolder.loading = false;
    }, dftFail);
    $('#show-week').dropdown();
});