$(document).ready(function() {
    uploadFile();
    $("#updateWish").click(function() {
        updateWish();
    });
});


function uploadFile() {
    $("#fileUpload").fileupload({
        url: Flask.url_for("uploadFile"),
        dataType: "json",
        add: function(e, data) {
            data.submit();
        },
        success: function(jsonData, status) {
            // 使用fileUpload插件时,fileupload函数中的success回调函数会自动将jsonData解析好,因此如果再继续使用response = JSON.parse(jsonData)就会出现`Unexpected token o in JSON at position`的错误,因为jsonData本身已经是object.
            var response = jsonData;
            var oldWishFilePath = $("#imgUpload").attr("src").slice(15,);
            deleteOldFile(oldWishFilePath);
            var filePath = response.fileName;
            $("#imgUpload").attr("src", "static/Uploads/" + filePath);
            $("#filePath").val(filePath);
            // 先进行一次预保存,防止用户在上传新图片后,没有点击保存,造成数据库中wish_file_path与Uploads文件夹中存储的文件无法对应一致,造成下次编辑时不能正确显示图片
            $.ajax({
                url: Flask.url_for("update_wish"),
                data: {
                    "wish_id": localStorage.getItem("editId"),
                    "title": $("#editTitle").val(),
                    "description": $("#editDescription").val(),
                    "filePath": $("#filePath").val(),
                    "accomplished": $("#isDone").prop("checked"),
                    "private": $("#isPrivate").prop("checked")
                },
                method: "POST",
                success: function(jsonData) {
                    var response = JSON.parse(jsonData);
                    console.log(response.status);

                },
                error: function(error) {
                    console.log(error);
                }
                    });
                },
            error: function(error) {
                console.log(error);
            }
    });
}


function deleteOldFile(oldWishFilePath) {
    var oldWishFilePath = oldWishFilePath;
    $.ajax({
        url: Flask.url_for("delete_old_file"),
        method: "POST",
        data: {"oldFile": oldWishFilePath},
        success: function(jsonData) {
            response = JSON.parse(jsonData);
            console.log(response.status);
        },
        error: function(error) {
            console.log(error);
        }
    });
}


function updateWish() {
    $.ajax({
        url: Flask.url_for("update_wish"),
        data: {
            "wish_id": localStorage.getItem("editId"),
            "title": $("#editTitle").val(),
            "description": $("#editDescription").val(),
            "filePath": $("#filePath").val(),
            "accomplished": $("#isDone").prop("checked"),
            "private": $("#isPrivate").prop("checked")
        },
        method: "POST",
        success: function(jsonData) {
            response = JSON.parse(jsonData);
            console.log(response.status);
            $("#editModal").modal("hide");
            getWishByPagination(1);
        },
        error: function(error) {
            console.log(error);
        }
});
}

