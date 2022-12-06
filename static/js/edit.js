function edit_cont() {
  let title = $("#title").val();
  // let cont = $("").val();
  $.ajax({
    type: "PUT",
    url: `/edit/{{list[0][0]}}`,
    data: { title: title },
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}