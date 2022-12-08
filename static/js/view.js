function delete_board(id, user_id) {
    $.ajax({
        type: "DELETE",
        url: `/board/${id}`,
        data: {},
        success: function (response) {
            alert(response["msg"]);
            window.location.href = "/board"
        },
    });
}