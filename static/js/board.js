function hit() {
  console.log('체크')
  $.ajax({
    type: "POST",
    url: "/hit/post",
    data: {},
    success: function(response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}