function delete_board(id) {
    $.ajax({
        type: "DELETE",
        url: `/board/delete/${id}`,
        data: {},
        success: function (response) {
            alert(response["msg"]);
            window.location.href = "/board"
        },
    });
}