var collegeCounter = 0;

var isUserLoggedIn = false;
var flashInterval;
$(document).ready(function() {
    $.get("/api/sync", function(data) {
        if(data['isLoggedIn'] == true) {
            $("#user-button").text(data['user_email']);
            $("#user-button-link").attr('href', "/profile");
            $("#logout-button").addClass("show--inline");
            $("#nav-bar-user-content").addClass("show");
        }
    });
});

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

$("#input-signup-button").click(function() {
    var fname = $("#input-login-fname").val();
    var lname = $("#input-login-lname").val();
    var city = $("#input-login-city").val();
    var region = $("#input-login-region").val();
    var email = $("#input-login-email").val();
    var password = $("#input-login-password").val();
    var data = {
        "fname": fname.toString(),
        "lname": lname.toString(),
        "city": city.toString(),
        "region": region.toString(),
        "email": email.toString(),
        "password": password.toString()
    };

    var dataString = JSON.stringify(data);
    $.ajax({
        url: '/api/signup',
        type: 'POST',
        data: dataString,
        dataType: 'json',
        contentType: "application/JSON, charset=utf-8",
        success: function(data) {
            alert("Response: " + data['status']);
        }
    });
});

$("#input-login-button").click(function() {
    var email = $("#input-login-email").val();
    var password = $("#input-login-password").val();
    var data = {
        "email": email.toString(),
        "password": password.toString()
    };

    var dataString = JSON.stringify(data);
    $.ajax({
        url: '/api/login',
        type: 'POST',
        data: dataString,
        dataType: 'json',
        contentType: "application/JSON, charset=utf-8",
        success: function(data) {
            if(data['status'] == "failure - incorrect password") {
                flash("Incorrect password. Please try again.", "bad");
            }
            if(data['status'] == "success") {
                flash("Successfully logged in.", "good");
                window.location.href = "/";
            }
        }
    });
});

function flash(text, type) {
    if(type == "bad") {
        $("body").prepend('<div id="flash-bad">' + text + '</div>');
    } else {
        $("body").prepend('<div id="flash-good">' + text + '</div>');
    }
}