const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
    } else {
      entry.target.classList.remove("show");
    }
  });
});

const hiddenElements = document.querySelectorAll(".hidden");

hiddenElements.forEach((element) => observer.observe(element));

window.addEventListener("DOMContentLoaded", function () {
  var projectTitle = document.getElementById("projectTitle");
  projectTitle.style.display = "block";

  setTimeout(function () {
    projectTitle.style.display = "none";
  }, 3000);
});
