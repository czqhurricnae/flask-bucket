function editWish(element) {
	$.ajax({
		url: Flask.url_for("get_wish_by_id"),
		method: "POST",
		data: {"id": $(element).attr("data-id")},
		success: function(jsonData) {
			var response = JSON.parse(jsonData);
            if (Object.keys(response.status)[0] == "0") {
                $(element).removeAttr("data-toggle");
                $(element).removeAttr("data-target");
                $("#editTitle").val(response.wish["title"]);
                $("#editDescription").val(response.wish["description"]);
                $("#imgUpload").attr("src", "static/Uploads/"+response.wish["filePath"]);
                $("#isDone").prop("checked", response.wish["accomplished"]);
                $("#isPrivate").prop("checked", response.wish["private"]);
                $("#editModal").modal();
                localStorage.setItem("editId", $(element).attr("data-id"));
            }
		},
		error: function(error) {
			console.log(error);
		}
	});
}
