document.addEventListener("DOMContentLoaded", function () {
  if (window.location.pathname.search("create") != -1) {
    let url = this.querySelector("input[name='url']");
    let image = this.querySelector("img");
    url.value = image.src;
  }
});
