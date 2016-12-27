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
    var week = (selected_week.selected_week);
    week = week.replace(/[^0-9]/g,'');
    api.get('/api/u/course/list', {open_id: urlParam.open_id, week:parseInt(week)}, function (data) {
        successHolder.loading = false;
        successHolder.loaded = true;
    }, dftFail);
    $('#show-week').dropdown();
});