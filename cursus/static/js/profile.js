/** @typedef {"account" | "token" | "update"} Page */
/** @typedef {{ "active_token": string, "id": string, "revoked_token": string }} TokenResponseType */

function _mountAccount() {
  console.log("account page mounted");

  return;
}

function _mountToken() {
  console.log("token page mounted");

  /**
   * @type {HTMLElement}
   */
  const generateToken = document.querySelector("#generate-btn");

  /**
   * @type {HTMLElement}
   */
  const revokeToken = document.querySelector("#revoke-btn");

  if (generateToken)
    generateToken.addEventListener("click", handleGenerateToken);

  if (revokeToken) revokeToken.addEventListener("click", handleRevokeToken);

  return;
}

function _mountUpdate() {
  console.log("update page mounted");

  return;
}

/**
 * Callback function to mount the fragment sub page to the DOM
 *
 * @param {HTMLElement} element
 * @param {string} innerHTML
 * @returns {void}
 */
function onMount(element, innerHTML) {
  element.innerHTML = innerHTML;
}

/**
 * Callback function after the page is mounted
 *
 * @param {Page} page
 * @returns {void}
 */
function onMounted(page) {
  if (page === "update") {
    _mountUpdate();
    return;
  } else if (page === "token") {
    _mountToken();
    return;
  }

  _mountAccount();
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

    const currentPage = window.location.pathname.split("/")[2];

    // Do nothing if the current page is the same as the page to be loaded
    if (currentPage === page) return;

    const xhr = new XMLHttpRequest();

    xhr.open("GET", `/profile/${page}`, true);
    xhr.setRequestHeader("X-Requested-SPA", "true");

    xhr.onload = function () {
      if (this.status === 200) {
        onMount(element, this.responseText);
        onMounted(page);

        window.history.pushState("", "", `/profile/${page}`);
      }
    };

    xhr.send();
  };
}

/**
 * Callback function to generate a new token on click
 *
 * @param {MouseEvent} e
 * @returns {void}
 */
function handleGenerateToken(e) {
  const xhr = new XMLHttpRequest();

  xhr.open("GET", "/profile/generate_token", true);

  xhr.onload = function () {
    if (this.status === 200) {
      /** @type {TokenResponseType} */
      const response = JSON.parse(this.responseText);

      const profileApiDisplay = document.querySelector("#profile-api-display");

      if (profileApiDisplay) {
        profileApiDisplay.innerHTML = `<p>${response.active_token}</p>`;
      }
    }
  };

  xhr.send();

  return;
}

/**
 * Callback function to revoke the currently active token on click
 *
 * @param {MouseEvent} e
 * @returns {void}
 */
function handleRevokeToken(e) {
  return;
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
    const page = window.location.pathname.split("/")[2];
    const xhr = new XMLHttpRequest();

    xhr.open("GET", `/profile/${page}`, true);
    xhr.setRequestHeader("X-Requested-SPA", "true");

    xhr.onload = function () {
      if (this.status === 200) {
        onMount(profileSpa, this.responseText);
        onMounted(page);

        loaded = true;
      }
    };

    xhr.send();
  }
})();
