const search_input = document.getElementById("search-product");
const search_block = document.querySelector(".search-info");

function openSearchBlock() {
  search_block.style.display = "block";
  search_input.style.borderRadius = "10px 10px 0 0";
}

function closeSearchBlock() {
  search_block.style.display = "none";
  search_input.style.borderRadius = "10px";
}

search_input.addEventListener("input", () => {
  if (search_input.value.length > 0) {
    openSearchBlock();
  } else {
    openSearchBlock();
  }
});

search_input.addEventListener("focus", () => {
  if (search_input.value.length > 0) {
    openSearchBlock();
  }
});

document.addEventListener("click", (e) => {
  if (!search_block.contains(e.target) && e.target !== search_input) {
    closeSearchBlock();
  }
});