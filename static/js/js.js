$(document).ready(function () {
    $.ajax({
        type: "GET", url: `/users`, data: {}, success: function (response) {
            console.log(1)
            const rows = response["users"];
            let name = rows['user_name']
            let email = rows["user_email"]
            let disc = rows["user_disc"]
            let img = rows["user_image"]
            let imgsrc = "../static/img/" + img
            console.log(1)
            let temp_html = `
        <div class="card mypage_midbox">
            <img src="${imgsrc}" id="user_image">
            <ul class="list-group list-group-flush">
            <li class="list-group-item mypage_email">이름 : ${name}</li>
            <li class="list-group-item mypage_disc">이메일 : ${email}</li>
            </ul>
            <div class="card-body">
            <h3 class="card-title mypage_name">${disc}</h3>
            </div>
        </div>
        <div class="glbtn">
            <button type="button" class="btn btn-outline-dark"><a href="/users/edit" class="card-link">프로필 수정</a></button>
            <button type="button" class="btn btn-outline-dark"><a href="/" class="card-link">홈으로</a></button>
        </div>`

            console.log(temp_html)
            $('.mypage_main').append(temp_html)
        }
    })
})