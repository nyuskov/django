document.addEventListener("DOMContentLoaded", function () {
  try {
    this.querySelectorAll("#header .menu li").classList.remove("selected");
  } catch {}
  try {
    if (window.location.pathname.search("blog") != -1) {
      this.querySelector("#blog").classList.add("selected");
    } else if (window.location.pathname.search("account") != -1) {
      this.querySelector("#dashboard").classList.add("selected");
    }
  } catch {}

  const closes = this.querySelectorAll(".close");

  for (let i = 0; i < closes.length; i++) {
    closes[i].addEventListener("click", function () {
      this.parentElement.style.display = "none";
    });
  }
});
