$(document).ready(function () {
    $("#logout").click(function () {
        $.ajax({
            type: "POST",
            url: `/logout`,
            data: {},
            success: function (response) {
                console.log(response["msg"]);
                alert("로그아웃 성공");
                window.location.href="/";
            }
        })
    })
})