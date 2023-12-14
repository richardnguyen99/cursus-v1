(function (window, document, undefined) {
  const navbarDropdown = document.getElementById("navbarDropdown");
  const navbarDropdownBtn = document.querySelector(".dropdown__btn");
  const modal = document.getElementById("modal");

  navbarDropdownBtn.addEventListener("click", function () {
    toggleDropdown("navbarDropdown");
  });

  modal.onclick = function (event) {
    event.preventDefault();

    if (event.target === modal) modal.classList.remove("modal--open");
  };

  /**
   * Handle global click events.
   *
   * @param {Event} event
   */
  window.onclick = function (event) {
    handleClickOutside(event); // from dropdown.js
  };
})(window, document);
