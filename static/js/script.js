$(document).ready(function () {
    $("#login").click(function () {
        const id = $("#inputId").val();
        const pw = $("#inputPassword").val();
        console.log("클릭1")
        $.ajax({
            type: "POST",
            url: `/login`,
            data: {
                id: id,
                pw: pw
            },
            success: function (response) {
                alert(response["msg"]);
                if (response["check"]) {
                    window.location.href = "/";
                } else {
                    window.location.reload();
                }

            }
        })
    })
})