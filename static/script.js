$(document).ready(function () {
    $("#login").click(function () {
        const id = $("#id").val();
        const pw = $("#password").val();

        $.ajax({
            type: "POST",
            url: `/login`,
            data: {
                id: id,
                pw: pw
            },
            success: function (response) {
                console.log(response["msg"]);
                alert("로그인 성공");
                window.location.href="/";
            }
        })
    })

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