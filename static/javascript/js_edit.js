$(document).ready(function () {
    const id = 1;
    $.ajax({
        type: "GET",
        url: `/users/${id}`,
        data: {},
        success: function (response) {
            const rows = response["users"];
            let name = rows['user_name']
            let email = rows["user_email"]
            let disc = rows["user_disc"]
            let img = rows["user_image"]
            let imgsrc = "../static/img/" + img
            let temp_html = `
    <div class="card mypage_midbox">
        <div class="qwer">
            <div class="myedit_img">
            <img src="${imgsrc}" id="user_image">
            </div>
                <label class="editlabel" for="img_edit">
                <div class="btn-upload">사진 업로드</div>
                </label>
                <input class="myedit_imgupload" type="file" id="img_edit" value="사진업로드"/>
                <button class="myedit_imgdel">
                    사진 삭제
                </button>
            </div>
            <ul class="list-group list-group-flush">
            <li class="list-group-item mypage_email">이름<br><br><input class="myedit_name" value="${name}" id="name_edit"></li>
            <li class="list-group-item mypage_disc">이메일<br><br><input class="myedit_email" value="${email}" id="email_edit"></li>
            </ul>
            <div class="card-body">
            <h3 class="card-title mypage_name">자기소개<br><br><textarea class="myedit_disc">${disc}</textarea></h3>
            </div>
        </div>
        <div class="glbtn">
            <button type="button" class="btn btn-outline-dark okbtn" id="profile_edit"><a href="/edit" class="card-link">확인</a></button>
            <button type="button" class="btn btn-outline-dark cancelbtn"><a href="/" class="card-link">취소</a></button>
        </div>`
            $('.myedit_main').append(temp_html)

            $("input[type=file]").change(function (event) {
                let tmpPath = URL.createObjectURL(event.target.files[0]);

                $("#user_image").attr("src", tmpPath);
            });

            $(".myedit_imgdel").click(function () {
                $("#user_image").attr("src", "../static/img/default.png");
            })

            $(".okbtn").click(function () {
                const name = $(".myedit_name").val();
                const email = $(".myedit_email").val();
                const disc = $(".myedit_disc").val();
                const imageInput = $("#img_edit")[0];
                const formData = new FormData();

                formData.append("name", name);
                formData.append("email", email);
                formData.append("disc", disc);
                formData.append("file", imageInput.files[0]);

                $.ajax({
                    type: "PUT",
                    url: `/users/${id}`,
                    processData: false,
                    contentType: false,
                    data: formData,
                    success: function (response) {
                        alert(response["msg"])
                        window.location.href = "/mypage"
                    }
                })
            })
        }
    })
})

