/**
 *
 * @param {HTMLElement} element
 * @param {string} innerHTML
 * @returns {void}
 */
function callback(element, innerHTML) {
  element.innerHTML = innerHTML;
}

/**
 *
 * @param {HTMLElement} element
 * @param {string} page
 * @returns {function(Event): void}
 */
function handleClick(element, page) {
  return function (e) {
    e.preventDefault();

    const xhr = new XMLHttpRequest();

    xhr.open("GET", `/profile/${page}`, true);
    xhr.setRequestHeader("X-Requested-SPA", "true");

    xhr.onload = function () {
      if (this.status === 200) {
        callback(element, this.responseText);

        window.history.pushState("", "", `/profile/${page}`);
      }
    };

    xhr.send();
  };
}

(function () {
  let loaded = false;

  /**
   * @type {HTMLElement}
   */
  const profileSpa = document.querySelector(".profile__spa");

  /**
   * @type {HTMLElement}
   */
  const accountLink = document.querySelector("#profile-link");

  /**
   * @type {HTMLElement}
   */
  const tokenLink = document.querySelector("#profile-token");

  /**
   * @type {HTMLElement}
   */
  const updateLink = document.querySelector("#profile-update");

  if (accountLink)
    accountLink.addEventListener("click", handleClick(profileSpa, "account"));

  if (tokenLink)
    tokenLink.addEventListener("click", handleClick(profileSpa, "token"));

  if (updateLink)
    updateLink.addEventListener("click", handleClick(profileSpa, "update"));

  if (profileSpa && !loaded) {
    const innerText = profileSpa.innerText;
    profileSpa.innerText = "";

    profileSpa.innerHTML = innerText;
    loaded = true;
  }
})();
