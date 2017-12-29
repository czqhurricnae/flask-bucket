function deleteWish(element) {
    localStorage.setItem("deleteId", $(element).attr("data-id"));
        $(element).removeAttr("data-toggle");
        $(element).removeAttr("data-target");
        $("#deleteModal").modal();
}

