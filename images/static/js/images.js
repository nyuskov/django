document.addEventListener("DOMContentLoaded", function () {
  if (window.location.pathname.search("create") != -1) {
    let url = this.querySelector("input[name='url']");
    let image = this.querySelector("img");
    url.value = image.src;
  } else if (window.location.pathname.search("detail") != -1) {
    let options = {
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      mode: "same-origin",
    };
    document.querySelector("a.like").addEventListener("click", function (e) {
      e.preventDefault();
      let likeButton = this;
      // add request body
      let formData = new FormData();
      formData.append("id", likeButton.dataset.id);
      formData.append("action", likeButton.dataset.action);
      options["body"] = formData;
      // send HTTP request
      fetch(url, options)
        .then((response) => response.json())
        .then((data) => {
          if (data["status"] === "ok") {
            let previousAction = likeButton.dataset.action;
            // toggle button text and data-action
            let action = previousAction === "like" ? "unlike" : "like";
            likeButton.dataset.action = action;
            likeButton.innerHTML =
              action === "like" ? gettext("Like") : gettext("Unlike");
            // update like count
            let likeCount = document.querySelector("span.count .total");
            let totalLikes = parseInt(likeCount.innerHTML);
            likeCount.innerHTML =
              previousAction === "like" ? totalLikes + 1 : totalLikes - 1;
          }
        });
    });
  } else {
    let page = 1;
    let emptyPage = false;
    let blockRequest = false;
    window.addEventListener("scroll", function (e) {
      let margin = document.body.clientHeight - window.innerHeight - 200;
      if (window.pageYOffset > margin && !emptyPage && !blockRequest) {
        blockRequest = true;
        page += 1;
        fetch("?images_only=1&page=" + page)
          .then((response) => response.text())
          .then((html) => {
            if (html === "") {
              emptyPage = true;
            } else {
              let imageList = document.getElementById("image-list");
              imageList.insertAdjacentHTML("beforeEnd", html);
              blockRequest = false;
            }
          });
      }
    });
    // Launch scroll event
    const scrollEvent = new Event("scroll");
    window.dispatchEvent(scrollEvent);
  }
});
