$(document).ready(function () {
    $("#login").click(function () {
        const id = $("#inputId").val();
        const pw = $("#inputPassword").val();

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
                window.location.href = "/";
            }
        })
    })
})