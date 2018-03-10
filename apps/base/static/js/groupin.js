$(function () {

    $(".breadcrumb > li:last > a").contents().unwrap();
    $(".breadcrumb > li:last").addClass("active");

});