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
    el: '#selected_week',
    data: {
        selected_week:
    }
})
var day_list = new Vue({
    el: '#day-list',
    data:{
        week:[
            {
                text: '周一',
                date: ''
            },
            {
                text: '周二',
                date:''
            },
            {
                text: '周三',
                date:''
            },
            {
                text: '周四',
                date:''
            },
            {
                text: '周五',
                date:''
            },
            {
                text: '周六',
                date:''
            },
            {
                text: '周日',
                date:''
            }
        ]
    }
})
$(function () {
    api.get('/api/u/course/list', {open_id: urlParam.open_id, week:}, function (data) {
        successHolder.loading = false;
        successHolder.loaded = true;
    }, dftFail);
    $('#show-week').dropdown();
});