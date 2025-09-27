const menuBtn = document.getElementById("menu-catalog-btn");
const menu = document.querySelector(".menu-bottom");

let firstOpen = true;

menuBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  menu.classList.toggle("active");

  if (menu.classList.contains("active") && firstOpen) {
    const firstCategory = document.querySelector(".category-btn");
    if (firstCategory) {
      activateCategory(firstCategory);
    }
    firstOpen = false;
  }
});

document.addEventListener("click", (e) => {
  if (!menu.contains(e.target) && e.target !== menuBtn) {
    menu.classList.remove("active");
  }
});

const categoryBtns = document.querySelectorAll(".category-btn");
const subcategories = document.querySelectorAll(".subcategory");
let hoverTimer;

function activateCategory(btn) {
  categoryBtns.forEach(b => {
    b.classList.remove("active_btn");
    const link = b.querySelector("a");
    if (link) {
      link.classList.remove("category-text-active");
      link.classList.add("category-btn-a");
    }
  });

  btn.classList.add("active_btn");
  const link = btn.querySelector("a");
  if (link) {
    link.classList.add("category-text-active");
    link.classList.remove("category-btn-a");
  }

  const targetId = btn.id;
  subcategories.forEach(sub => {
    if (sub.getAttribute("name") === targetId) {
      sub.style.display = "block";
    } else {
      sub.style.display = "none";
    }
  });
}

categoryBtns.forEach(btn => {
  btn.addEventListener("mouseenter", () => {
    hoverTimer = setTimeout(() => activateCategory(btn), 250);
  });

  btn.addEventListener("mouseleave", () => {
    clearTimeout(hoverTimer);
  });

  btn.addEventListener("click", (e) => {
    e.preventDefault();
    activateCategory(btn);
  });
});