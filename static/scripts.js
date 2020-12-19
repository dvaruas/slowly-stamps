$("#new-category").change(function() {
  if ($("#new-category").prop("checked") == true) {
    $("#newCategoryTextArea").prop("disabled", false);
  } else {
    $("#newCategoryTextArea").prop("disabled", true);
  }
});

$(".deletePalBtn").click(function() {
  $(".selectStampsList").removeClass("bg-secondary");
  $(".selectStampsList").removeClass("text-white");
  $(".selectStampsList").addClass("text-dark");
  
  let id = $(this).attr("id");
  let userId = id.substring(10);
  $("#user-detail-alert-text").html("Are you sure you wish to delete this user? All data will be lost forever!");
  $("#user-detail-alert-confirm").attr("href", `/delete/${userId}`);
  $("#user-detail-alert").removeClass("d-none");
});

$("#user-detail-alert-close").click(function() {
  $("#user-detail-alert").addClass("d-none");

  $(".selectStampsList").removeClass("bg-secondary");
  $(".selectStampsList").removeClass("text-white");
  $(".selectStampsList").addClass("text-dark");
});

$(".selectStampsList").click(function() {
  let id = $(this).attr("id");
  let stampID = id.substring(12);

  let uid = $(".deletePalBtn").attr("id");
  let userId = uid.substring(10);

  $(".selectStampsList").removeClass("bg-secondary");
  $(".selectStampsList").removeClass("text-white");
  $(".selectStampsList").addClass("text-dark");
  $(this).removeClass("text-dark");
  $(this).addClass("text-white");
  $(this).addClass("bg-secondary");

  $("#user-detail-alert-text").html("Do you wish to use the selected stamp for this user?");
  $("#user-detail-alert-confirm").attr("href", `/use/${userId}-${stampID}`);
  $("#user-detail-alert").removeClass("d-none");
});
