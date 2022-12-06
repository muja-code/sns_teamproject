function delete_board(num) {
  $.ajax({
    type: "DELETE",
    url:  `/${num}`,
    data: {},
    success: function (response) {
      alert(response["msg"]);
      window.location.href="/board"
    },
  });
}