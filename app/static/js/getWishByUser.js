// jQuery判断DOM节点是否存在于页面中
(function ($) {
    $.fn.exist = function () {
        if ($(this).length >= 1) {
            return true;
        }
        return false;
    };
})(jQuery);

var getWishByPagination = function (p_pageNumber) {
    // itemsPerPage
    var itemsPerPage = 1;
    var _offset = (p_pageNumber - 1) * itemsPerPage;

    $.ajax({
        url: Flask.url_for("get_wish_by_user_to_paginate"),
        method: "POST",
        data: {"offset": _offset},
        success: function (jsonData) {
            var response = JSON.parse(jsonData);
            if (( Object.keys(response[0].status)[0] != "1" ) && ( Object.keys(response[0].status)[0] != "2")) {
                $(".jumbotron").hide();

                var wishsList = $("<div>").attr("class", "row").append(
                    $("<div>").attr("class", "col-md-12").append(
                        $("<div>").attr("class", "panel-body").append(
                            $("<ul>").attr("class", "list-group").attr("id", "ulist"))));

                if (!$(".pagination").exist()) {
                  var pagination = $("<nav>").append($("<ul>").attr("class", "pagination"));
                }

                $(".pagination").empty();

                var total = response[2]["Total"];
                var pageCount = total / itemsPerPage;
                var pageReminder = total % itemsPerPage;
                var pageStart = Number($("#hdnStart").val());
                var pageEnd = Number($("#hdnEnd").val());

                if (pageReminder) {
                    pageCount = Math.floor(pageCount) + 1;
                }

                // Append wishsList element after header element
                if (!$(".row").exist()) {
                    $(".header").after(wishsList);
                }

                // Append pagination element after wishsList element
                $("div.panel-body").after(pagination);

                /* No previous button link will be shown when displaying pages
                * 1 to 5.If the pages displayed are greater than 5 then we'll
                * display the previous button link. */
                if (pageStart > 5) {
                    var aPrevious = $("<a>").attr({"href": "#"}, {"aria-label": "Previous"}).append($("<span>").attr("aria-hidden", "true").html("&laquo;"));
                    $(aPrevious).click(function () {
                        /* When the user clicks the previous button, we'll reset the hdnStart and hdnEnd values and call the getWishByPagination JavaScript function. */
                        $("#hdnStart").val(pageStart - 5);
                        $("#hdnEnd").val(pageStart - 5 + 4);
                        getWishByPagination(pageStart - 5);
                    });
                    var previousLink = $("<li>").append(aPrevious);
                    $(".pagination").append(previousLink);
                }

                for (i = pageStart; i <= pageEnd; i++) {
                    if (i > pageCount) {
                        break;
                    }
                    else {
                        var aPage = $("<a>").attr("href", "#").text(i);
                        aPage.click(function (i) {
                            return function () {
                                getWishByPagination(i);
			    }
                        }(i));
                        var page = $("<li>").append(aPage);
                        if (p_pageNumber == i) {
                          $(page).attr("class", "active");
                        }
                        $(".pagination").append(page);
                    }
                }

                if (pageEnd < pageCount) {
                    // var aNext = $( "<a>" ).attr( { "href": "#" }, { "aria-label": "Next" } ).append( $( "<span>" ).attr( "aria-hidden": "true" ).html( "&raquo;" ) );
                    var aNext = $("<a>").attr({"href": "#"}, {"aria-label": "Previous"}).append($("<span>").attr("aria-hidden", "true").html("&raquo;"));
                    $(aNext).click(function () {
                        $("#hdnStart").val(pageStart + 5);
                        $("#hdnEnd").val(pageStart + 5 + 4);
                        getWishByPagination(pageStart + 5);
                    });
                    var nextLink = $("<li>").append(aNext);
                    $(".pagination ").append(nextLink);
                }

                $("#ulist").empty();

                // Append to the template
                $("#listTemplate").tmpl(response[1]).appendTo("#ulist");
            }
          else {
            $("div.row").empty();
            $(".jumbotron").show();
          }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

      // [> var div = $("<div>").attr("class", "list-group") <]
      // .append($("<a>").attr("class", "list-group-item active").append($("<h4>").attr("class", "list-group-heading"),$("<p>").attr("class", "list-group-item-text")));
      // $.each(response, function(index, value){
      // var wish = $(div).clone();
      // $(wish).find("h4").text(value.Title);
      // $(wish).find("p").text(value.Description);
      // $(".jumbotron").append(wish);
      // [> }); <]

      // var wishsList = $("<div>").attr("class", "row").append(
      // $("<div>").attr("class", "col-md-12").append(
      // $("<div>").attr("class", "panel-body").append(
      // $("<ul>").attr("class","list-group").attr("id", "ulist"))));

      // var pagination =$("<nav>").append($("<ul>").attr("class", "pagination"));

      // var prevLink = $("<li>").append($("<a>").attr({"href": "#"}, {"aria-label": "Previous"}).append($("<span>").attr("aria-hidden", "true").html("&laquo;")));

      // var nextLink = $("<li>").append($("<a>").attr({"href": "#"}, {"aria-label": "Next"}).append($("<span>").attr("aria-hidden", "true").html("&raquo;")));

$(document).ready(
    function () {
        /* getWishByUser(); */
        getWishByPagination(1);
    }
);
