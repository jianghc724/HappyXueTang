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
        view_status:0,
        status:1,
        teacher:"",
        email:"",
        my_comment:{
            "comment":"",
            "rating_one":0,
            "rating_two":0,
            "rating_three":0,
        },
        ratings:[],
        rating_texts:["课堂氛围：","课程收获：", "课程负担："],
        notices:[],
        notice_length:0,
        homeworks:[],
        homework_length:0,
        comments:[],
        comment_length:0,
        comment_last:[],
        files:[],
        remain:[]
    },
    methods:{
        getNotice:function(){
            api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id, status:1}, function (data) {
                course_meta.notices = data["notice_detail"];
                course_meta.notice_length = data["notice_detail"].length;
            }, dftFail);
        },
        getHomework:function(){
            api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id,status:2}, function (data) {
                course_meta.homeworks = data["new_operations"];
                course_meta.homework_length = data["new_operations"].length;
                course_meta.remain = new Array();
                for(var i = 0; i < course_meta.homework_length; i++){
                    var cur_remain = new Array(3);
                    var current_date = new Date(course_meta.homeworks[i].current_time*1000);
                    var due_date = new Date(course_meta.homeworks[i].duedate);
                    var time = (due_date.getTime() - current_date.getTime())/1000;
                    cur_remain[0] = Math.floor(time/86400);
                    cur_remain[1] = Math.floor(time%86400/3600);
                    cur_remain[2] = Math.floor(time%86400%3600/60);
                    course_meta.remain.push(cur_remain);
                }
            }, dftFail);
        },
        setNotice:function(){
            course_meta.status = 1;
        },
        setHomework:function(){
            course_meta.status = 2;
        },
        setComment:function(){
            course_meta.status = 3;
        },
        getTime:function(time){
            var date = new Date(time).toJSON();
            var date_array = date.split('T');
            var time_array = (date_array[1].split('.'))[0].split(':');
            return_time = date_array[0] + " " + time_array[0] + ":" + time_array[1] + ":"+ time_array[2];
            return return_time;
        },
        submit: function() {
            if(this.checkComment){
                var formData = JSON.stringify(this.my_comment);
                api.post('/api/u/course/comments/makecomment',{open_id: urlParam.open_id, course_id:urlParam.course_id,rating_one:formData.rating_one, rating_two:formData.rating_two,rating_three:formData.rating_three, comment:formData.comment})
            }
        },
        checkComment:function(){
            if(this.my_comment != "")
                return true;
            else
                return false;
        }
    }
})

$(function () {
    api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id,status:0}, function (data) {
        course_meta.view_status = data['status'];
        course_meta.name = data["name"];
        course_meta.teacher = data["teacher"];
        course_meta.email = data["email"];
        api.get('/api/u/course/comments/overview', {open_id: urlParam.open_id, course_id:urlParam.course_id}, function (data) {
            var current_time = data['current_time'];
            course_meta.ratings = data["ratings"];
            for(var i = 0; i < 3; i++){
                course_meta.ratings[i] = Math.round(course_meta.ratings[i]);
                if(course_meta.ratings[i] < 0)
                    course_meta.ratings[i] = 0;
            }
            course_meta.comments = data["comments"];
            course_meta.comment_length = data["comments"].length;
            for(var i = 0; i < course_meta.comment_length; i++){
                    var cur_last = new Array(3);
                    var current_date = new Date(current_time*1000);
                    var due_date = new Date(course_meta.comments[i].time);
                    var time = (due_date.getTime() - current_date.getTime())/1000;
                    cur_last[0] = Math.floor(time/86400);
                    cur_last[1] = Math.floor(time%86400/3600);
                    cur_last[2] = Math.floor(time%86400%3600/60);
                    course_meta.comment_last.push(cur_last);
                }
        }, dftFail);
        course_meta.getNotice();
        course_meta.getHomework();
        successHolder.loading = false;
        $("#my-rating2").rating({
        initialRating:1,
        maxRating: 5
    });
    }, dftFail);
});