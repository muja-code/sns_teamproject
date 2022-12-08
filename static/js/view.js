function delete_board(num) {
  $.ajax({
    type: "DELETE",
    url:  `/board/${num}`,
    data: {},
    success: function (response) {
      alert(response["msg"]);
      window.location.href="/board"
    },
  });
}