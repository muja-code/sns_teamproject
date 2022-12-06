// $(document).ready(function(){
//   $.ajax({
//     type: "GET",
//     url: "/board",
//     data: {},
//     success: function(response) {
//       window.location.reload();
//     }
//   })
// })



function hit() {
  console.log('체크')
  $.ajax({
    type: "POST",
    url: "/board/{{ i[0] }}",
    data: {},
    success: function(response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}