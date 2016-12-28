var successHolder = new Vue({
    el: '#successHolder',
    data: {
        loading:true,
        
    }
})
var course_meta = new Vue({
    el:"#course-meta",
    data:{
        loaded:false,
        name:"",
        status:0,
        teacher:"",
        email:"",
        ratings:[],
        rating_texts:["课堂氛围：","课程收获：", "课程负担："]
    }
})

$(function () {
    console.log(urlParam.course_id);
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
            successHolder.loading = false;
            course_meta.loaded = true;
        }, dftFail);
    }, dftFail);
    $('#show-week').dropdown();
});