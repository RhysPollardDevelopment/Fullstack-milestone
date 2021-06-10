$(document).ready(function () {
    bindEvents();
});

function bindEvents() {
    $(".btn-danger.delete").on('click', function () {
        confirm_delete($(this).attr('data-info'));
    });
}

function confirm_delete(recipe_delete_url) {
    $("#deleteConfirm").modal("show");
    $("#confirm").on("click", function () {
        window.location.href = recipe_delete_url;
    });
    $("#cancel").on("click", function () {
        $("#deleteConfirm").modal("hide");
    });
}