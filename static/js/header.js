const menuBtn = document.getElementById("menu-catalog-btn");
const menu = document.querySelector(".menu-bottom-container");

let firstOpen = true;

// Скрыть все подкатегории при загрузке
const subcategories = document.querySelectorAll(".subcategory");
subcategories.forEach(sub => {
  sub.style.display = "none";
});

// Функция для установки translateY с учётом высоты контейнера, кнопки и 65px
function setTranslate(initial = false) {
  const buttonHeight = menuBtn.offsetHeight;
  const containerHeight = menu.offsetHeight;
  const translateY = -(containerHeight - buttonHeight);
  menu.style.transform = `translateY(${translateY}px)`;

  if (initial) {
    requestAnimationFrame(() => {
      menu.classList.add("ready");
    });
  }
}

// Устанавливаем позицию сразу при загрузке (без анимации)
window.addEventListener("load", () => setTranslate(true));
window.addEventListener("resize", () => setTranslate(false));

menuBtn.addEventListener("click", (e) => {
  e.stopPropagation();

  if (menu.classList.contains("active")) {
    setTranslate();
    menu.classList.remove("active");
  } else {
    menu.style.transform = "translateY(0)";
    menu.classList.add("active");

    // При первом открытии активируем первую категорию
    if (firstOpen) {
      const firstCategory = document.querySelector(".category-btn");
      if (firstCategory) {
        activateCategory(firstCategory);
      }
      firstOpen = false;
    }
  }
});

// Закрытие при клике вне меню
document.addEventListener("click", (e) => {
  if (!menu.contains(e.target) && e.target !== menuBtn) {
    setTranslate();
    menu.classList.remove("active");
  }
});

// Логика категорий и подкатегорий
const categoryBtns = document.querySelectorAll(".category-btn");
let hoverTimer;

function activateCategory(btn) {
  // Сброс у всех категорий
  categoryBtns.forEach(b => {
    b.classList.remove("active_btn");
    const link = b.querySelector("a");
    if (link) {
      link.classList.remove("category-text-active");
      link.classList.add("category-btn-a");
    }
  });

  // Установка активной категории
  btn.classList.add("active_btn");
  const link = btn.querySelector("a");
  if (link) {
    link.classList.add("category-text-active");
    link.classList.remove("category-btn-a");
  }

  // Показ только нужной подкатегории
  const targetId = btn.id;
  subcategories.forEach(sub => {
    if (sub.getAttribute("name") === targetId) {
      sub.style.display = "block";
    } else {
      sub.style.display = "none";
    }
  });

  // Пересчитать смещение на случай изменения высоты подкатегорий
  if (!menu.classList.contains("active")) setTranslate();
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