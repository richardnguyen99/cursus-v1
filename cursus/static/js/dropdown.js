/**
 * Toggle the dropdown menu with the given id.
 *
 * @param {string} dropdownId
 */
function toggleDropdown(dropdownId) {
  let dropdown = document.getElementById(dropdownId);
  let dropdownMenu = dropdown.querySelector(".dropdown__menu");

  console.log(dropdownMenu);

  dropdown.setAttribute(
    "aria-expanded",
    dropdownMenu.classList.contains("dropdown--show") ? "false" : "true"
  );

  dropdownMenu.classList.toggle("dropdown--show");
}

/**
 * Close all dropdown menus when clicking outside of them.
 *
 * @param {Event} e
 */
function handleClickOutside(event) {
  // Handle closing of dropdown menus when clicking outside
  if (!event.target.matches(".dropdown__btn")) {
    const dropdowns = document.getElementsByClassName("dropdown__menu");

    for (let dropdown of dropdowns) {
      if (dropdown.classList.contains("dropdown--show")) {
        dropdown.classList.remove("dropdown--show");

        const parent = dropdown.parentElement;
        parent.setAttribute("aria-expanded", "false");
      }
    }
  }
}
