function confirmDeleteWish(element) {
	$.ajax({
		url: Flask.url_for("deleteWish"),
		data: {"id": localStorage.getItem("deleteId")},
		method: "POST",
		success: function(jsonData) {
            var response = JSON.parse(jsonData);
            deleteOldFile(response.wishFilePath);
            if (Object.keys(response.status)[0] == "0") {
                $("#deleteModal").modal("hide");
                getWishByPagination(1);
            }
            else {
                $(element).parent().prev().html('<p style="color:red;">Error occured!!</p>');
      }
	},
		error: function(error) {
			console.log(error);
		}
	});
}


function deleteOldFile(oldWishFilePath) {
    var oldWishFilePath = oldWishFilePath;
    $.ajax({
        url: Flask.url_for("deleteOldFile"),
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

