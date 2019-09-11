var obj = null;

$(function(){
    // 点击"删除"按钮触发
    $(".delete").on("click",function(){
        obj = $(this);
        changeDLGContent("你确定要删除用户【"+obj.attr("username")+"】吗？");
        openYesOrNoDLG();
    });
    // 点击提示框中的"取消"按钮触发
    $('#no').click(function () {
        $('.zhezhao').css('display', 'none');
        $('#removeUse').fadeOut();
    });
    // 点击提示框中的"确定"按钮触发
    $('#yes').click(function () {
        deleteExecute(obj);
    });
});

//发送ajax请求删除内容
function deleteExecute(obj){
    $.ajax({
        type:"GET",
        url:path+"/delete/delUser",
        data:{
            id:obj.attr("userid")
        },
        dataType:"json",
        success:function(data){
            // 一些提示信息
            changeDLGContent("对不起，删除用户【"+obj.attr("username")+"】失败");
        },
        error:function(data){
            //一些错误提示信息
            changeDLGContent("对不起，删除失败");
        }
    });
}

// 显示提示框
function openYesOrNoDLG(){
    $('.zhezhao').css('display', 'block');
    $('#removeUse').fadeIn();
}

// 改变提示内容
function changeDLGContent(contentStr){
    var p = $(".removeMain").find("p");
    p.html(contentStr);
}