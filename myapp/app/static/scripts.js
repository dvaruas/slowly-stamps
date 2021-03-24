$("#new-category").change(function() {
  if ($("#new-category").prop("checked") == true) {
    $("#newCategoryTextArea").prop("disabled", false);
  } else {
    $("#newCategoryTextArea").prop("disabled", true);
  }
});

$("#staticBackdrop").on("show.bs.modal", function(e) {
  $(".selectStampsList").removeClass("bg-secondary");
  $(".selectStampsList").removeClass("text-white");
  $(".selectStampsList").addClass("text-dark");

  let uid = $(".deletePalBtn").attr("id");
  let userId = uid.substring(10);
  let userName = $(".user-name").html();

  if ($(e.relatedTarget).hasClass("deletePalBtn")) {
    let imageHref = "/static/user-placeholder.jpg";

    let uImageId = $(".user-image").attr("id");
    if (uImageId != undefined) {
      let userImageId = uImageId.substring(5);
      imageHref = `/user_image/${userImageId}`;
    }

    $("#common-modal-body").html(`
      <table>
        <tr>
          <td>
            <img src="${imageHref}" height="100" width="100">
          </td>
          <td  style="padding:20px">
            <span>Are you sure you wish to delete <b>${userName}</b>? Beware, all data will be lost forever!</span>
          </td>
        </tr>
      </table>`);
    $("#common-modal-confirm-btn").removeClass("btn-primary").addClass("btn-danger");
    $("#common-modal-confirm-link").attr("href", `/delete/${userId}`);

  } else if ($(e.relatedTarget).hasClass("selectStampsList")) {
    let id = e.relatedTarget.id;
    let stampID = id.substring(12);

    let stampHref = `/static/stamp-placeholder.png`;
    let sImageId = $(e.relatedTarget).children("img").attr("id");
    if (sImageId != undefined ) {
      let stampImageId = sImageId.substring(6);
      stampHref = `/stamp_image/${stampImageId}`;
    }
    let stampName = $(e.relatedTarget).find("h5").html();

    $(e.relatedTarget).removeClass("text-dark");
    $(e.relatedTarget).addClass("text-white");
    $(e.relatedTarget).addClass("bg-secondary");

    $("#common-modal-body").html(`
      <table>
        <tr>
          <td>
            <img src="${stampHref}" height="100" width="100">
          </td>
          <td  style="padding:20px">
            <span>Are you sure you wish to use stamp <b>${stampName}</b> for your pal <b>${userName}</b></span>?
          </td>
        </tr>
      </table>`);
    $("#common-modal-confirm-link").attr("href", `/use/${userId}-${stampID}`);
  }
});

$("#common-modal-cancel-btn").click(function() {
  $(".selectStampsList").removeClass("bg-secondary");
  $(".selectStampsList").removeClass("text-white");
  $(".selectStampsList").addClass("text-dark");
});
