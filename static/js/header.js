const menuBtn = document.getElementById("menu-catalog-btn");
const menuBottom = document.querySelector(".menu-bottom");
const menuContainer = document.querySelector(".menu-bottom-container");
let firstOpen = true;
let isVisible = false;

menuBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    if (!isVisible) {
        openMenu();
    } else {
        closeMenu();
    }
});

function openMenu() {
    menuBottom.style.display = "block";
    menuBottom.style.maxHeight = "0px";
    requestAnimationFrame(() => {
        menuBottom.style.maxHeight = menuBottom.scrollHeight + "px";
    });
    isVisible = true;

    if (firstOpen) {
        const firstCategory = document.querySelector(".category-btn");
        if (firstCategory) activateCategory(firstCategory);
        firstOpen = false;
    }
}

function closeMenu() {
    menuBottom.style.maxHeight = "0";
    menuBottom.addEventListener("transitionend", function handler() {
        menuBottom.style.display = "none";
        menuBottom.removeEventListener("transitionend", handler);
    });
    isVisible = false;
}

const categoryBtns = document.querySelectorAll(".category-btn");
const subcategories = document.querySelectorAll(".subcategory");

function activateCategory(btn) {
    categoryBtns.forEach(b => b.classList.remove("active_btn"));
    btn.classList.add("active_btn");

    const targetId = btn.id;
    subcategories.forEach(sub => {
        sub.style.display = sub.dataset.parent === targetId ? "block" : "none";
    });
}

// Добавляем задержку для наведения
categoryBtns.forEach(btn => {
    let hoverTimer;

    btn.addEventListener("mouseenter", () => {
        hoverTimer = setTimeout(() => {
            activateCategory(btn);
        }, 20); // задержка 20 мс
    });

    btn.addEventListener("mouseleave", () => {
        clearTimeout(hoverTimer); // если курсор ушел раньше, таймер отменяется
    });
});

// Закрытие при клике вне контейнера
document.addEventListener("click", (e) => {
    if (isVisible && !menuContainer.contains(e.target) && e.target !== menuBtn) {
        closeMenu();
    }
});
