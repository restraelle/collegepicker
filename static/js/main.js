var collegeCounter = 0;

$(".compare-item").on("click", function() {
    id = $(this).attr("id");
    colData = null;
    if($(this).hasClass("flagged")) {
        $("#" + id + "-compare").remove();
        $(this).removeClass("flagged");
        collegeCounter -= 1;
    } else {
        if(collegeCounter < 4) {
            collegeCounter += 1;
            $(this).addClass("flagged");
            $.get("/api/get/college/" + id, function(data, status) {
                colData = data;
                item = '<div class="compare-table" id="' + colData['id'] + '-compare">';
                item += '<div class="compare-table-attribute compare-table-picture" style="background-image: url(\'' + colData['image_url'] + '\')"></div>';
                item += '<div class="compare-table-attribute"><p class="compare-table-attribute-title">' + colData['name'] + '</p></div>';
                item += '<div class="compare-table-attribute"><p class="compare-table-attribute-title">' + colData['location'] + '</p></div>';
                item += '<div class="compare-table-attribute"><p class="compare-table-attribute-title">' + colData['established_year'] + '</p></div>';
                item += '<div class="compare-table-attribute"><p class="compare-table-attribute-title">' + colData['acceptance_rate'] + '%</p></div>';
                item += '<div class="compare-table-attribute"><p class="compare-table-attribute-title">' + colData['minimum_gpa'] + '</p></div>';
                item += '<div class="compare-table-attribute"><p class="compare-table-attribute-title">' + colData['minimum_sat'] + '</p></div>';
                item += '<div class="compare-table-attribute"><p class="compare-table-attribute-title">' + colData['minimum_act'] + '</p></div>';
                item += '</div>';
                $(".compare-table").last().after(item);
            });
        }
    }

});