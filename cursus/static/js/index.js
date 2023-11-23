(function (window, document, undefined) {
  const navbarDropdown = document.getElementById("navbarDropdown");
  const navbarDropdownBtn = document.querySelector(".dropdown__btn");

  navbarDropdownBtn.addEventListener("click", function () {
    toggleDropdown("navbarDropdown");
  });

  /**
   * Handle global click events.
   *
   * @param {Event} event
   */
  window.onclick = function (event) {
    handleClickOutside(event); // from dropdown.js
  };
})(window, document);
