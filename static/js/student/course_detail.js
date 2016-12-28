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
        email:""
    }
})

$(function () {
    console.log(urlParam.course_id);
    api.get('/api/u/course/detail', {open_id: urlParam.open_id, course_id:urlParam.course_id,status:0}, function (data) {
        console.log(data);
        course_meta.name = data["name"];
        course_meta.status = data["status"];
        course_meta.teacher = data["teacher"];
        course_meta.email = data["email"];
        successHolder.loading = false;
        course_meta.loaded = true;
    }, dftFail);
    $('#show-week').dropdown();
});