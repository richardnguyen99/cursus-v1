/** @typedef {"account" | "token" | "update"} Page */
/** @typedef {{ "active_token": string, "id": string, "revoked_token": string }} TokenResponseType */

let actionMessageTimeoutId = null;

/**
 *
 * @param {MouseEvent} e
 */
function handleCancelDisplayName(e) {
  e.preventDefault();

  const inputElement = document.getElementById(
    e.currentTarget.getAttribute("data-cursus-field-cancel-at")
  );

  if (!inputElement) return;

  const submitBtn = document.getElementById(
    inputElement.getAttribute("data-cursus-submit-by")
  );

  inputElement.value = inputElement.getAttribute("data-cursus-init-value");

  e.currentTarget.classList.add("display-none");

  if (submitBtn) {
    submitBtn.classList.add("btn--secondary");
    submitBtn.classList.remove("btn--primary");
  }
}

/**
 *
 * @param {MouseEvent} e
 */
function handleSubmitDisplayName(e) {
  e.preventDefault();
}

/**
 *
 * @param {Event} e
 */
function handleChangeDisplayName(e) {
  e.preventDefault();

  const id = e.currentTarget.getAttribute("id");
  const displayName = e.currentTarget.value;
  const initialDisplayName = e.currentTarget.getAttribute(
    "data-cursus-init-value"
  );

  const resetBtn = document.getElementById(
    e.currentTarget.getAttribute("data-cursus-reset-by")
  );

  /**
   * @type {HTMLButtonElement}
   */
  const submitBtn = document.getElementById(
    e.currentTarget.getAttribute("data-cursus-submit-by")
  );

  const feedback = document.querySelector(
    `.profile__field__input-feedback[for="${id}"]`
  );

  if (displayName === initialDisplayName) {
    if (resetBtn) resetBtn.classList.add("display-none");

    if (submitBtn) {
      submitBtn.classList.add("btn--secondary");
      submitBtn.classList.remove("btn--primary");
    }
  } else {
    if (resetBtn) resetBtn.classList.remove("display-none");

    if (submitBtn) {
      submitBtn.classList.remove("btn--secondary");
      submitBtn.classList.add("btn--primary");
    }

    if (feedback) {
      if (displayName.length < 1 || displayName.length > 32) {
        feedback.classList.remove("profile--success");
        feedback.classList.add("error", "show");
        feedback.innerText = "Must be between 1 and 32 characters";

        submitBtn.classList.add(".disabled");
        submitBtn.disabled = true;
      } else {
        feedback.classList.remove("success", "error", "show");
        feedback.innerText = "";

        submitBtn.classList.remove(".disabled");
        submitBtn.disabled = false;
      }
    }
  }
}

/**
 *
 * @param {MouseEvent} e
 */
function handleUpdateDisplayName(e) {
  e.preventDefault();

  const input = document.getElementById(
    e.currentTarget.getAttribute("data-cursus-field-submit-at")
  );

  const value = input.value;
  const initValue = input.getAttribute("data-cursus-init-value");

  if (value === initValue) return;

  console.log(encodeURI(`/profile/update_display_name/${value}`));
}

function _mountAccount() {
  document.title = "Account - Profile - Cursus";

  const displayNameCancelBtn = document.getElementById(
    "profile-display-cancel-name-btn"
  );

  const displayNameSubmitBtn = document.getElementById(
    "profile-display-submit-name-btn"
  );

  if (displayNameCancelBtn)
    displayNameCancelBtn.addEventListener("click", handleCancelDisplayName);

  if (displayNameSubmitBtn)
    displayNameSubmitBtn.addEventListener("click", handleUpdateDisplayName);

  return;
}

function _mountToken() {
  document.title = "Tokens - Profile - Cursus";
  /**
   * @type {HTMLElement}
   */
  const generateToken = document.querySelector("#generate-btn");

  /**
   * @type {HTMLElement}
   */
  const revokeToken = document.querySelector("#revoke-btn");

  const copyToken = document.querySelector("#copy-token-btn");

  if (generateToken)
    generateToken.addEventListener("click", handleGenerateToken);

  if (revokeToken) revokeToken.addEventListener("click", handleRevokeToken);

  if (copyToken) copyToken.addEventListener("click", handleCopyToken);

  return;
}

function _mountHistory() {
  document.title = "History - Profile - Cursus";

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
  if (page === "history") {
    _mountHistory();
    return;
  } else if (page === "token") {
    _mountToken();
    return;
  }

  _mountAccount();

  const profile_fields = document.querySelectorAll(
    ".profile__field__input > input"
  );

  profile_fields.forEach((field) => {
    field.addEventListener("input", handleChangeDisplayName);
  });
}

/**
 * Update the navigation tab to reflect the current page
 *
 * @param {Page} page
 */
function updateNavTab(page) {
  const navTabs = document.querySelect;
}

/**
 *
 * @param {HTMLElement} spaContainer
 * @param {string} page
 * @returns {function(Event): void}
 */
function handleClick(spaContainer, page) {
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
        onMount(spaContainer, this.responseText);
        onMounted(page);

        const navTabs = document.querySelectorAll(".profile__nav-item");

        navTabs.forEach((tab) => {
          tab.classList.remove("profile--active");
        });

        if (page === "account") {
          navTabs[0].classList.add("profile--active");
        } else if (page === "token") {
          navTabs[1].classList.add("profile--active");
        } else {
          navTabs[2].classList.add("profile--active");
        }

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
    const profileApiDisplay = document.querySelector("#profile-api-display");
    const profileTokenActionMessage = document.querySelector(
      "#token-action-message"
    );

    const response = JSON.parse(this.responseText);

    if (this.status === 200) {
      if (profileApiDisplay) {
        profileApiDisplay.innerHTML = `<p>${response.active_token}</p>`;
      }

      if (profileTokenActionMessage) {
        profileTokenActionMessage.innerHTML = `<p class="profile--success">${response.message}</p>`;
      }
    }

    if (this.status === 403) {
      if (profileTokenActionMessage) {
        profileTokenActionMessage.innerHTML = `<p class="profile--danger">${response.message}</p>`;
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
  const xhr = new XMLHttpRequest();
  const apiToken = document.querySelector("#profile-api-display p");

  if (apiToken.innerText === "No active token") return;

  xhr.open("GET", "/profile/revoke_token", true);

  xhr.onload = function () {
    const response = JSON.parse(this.responseText);

    if (this.status === 200) {
      /** @type {TokenResponseType} */

      const profileApiDisplay = document.querySelector("#profile-api-display");

      if (profileApiDisplay) {
        profileApiDisplay.innerHTML = `<p>No active token</p>`;
      }
    }
  };

  xhr.send();

  return;
}

/**
 * Callback function to copy the token to the clipboard on click
 *
 * @param {MouseEvent} e
 */
function handleCopyToken(e) {
  const actionMessage = document.querySelector("#token-action-message");
  const apiToken = document.querySelector("#profile-api-display p");

  const tooltip = e.currentTarget.children[0];
  const btnWrapper = e.currentTarget.children[1];

  if (actionMessageTimeoutId) {
    clearTimeout(actionMessageTimeoutId);
    actionMessageTimeoutId = null;
  }

  actionMessageTimeoutId = setTimeout(() => {
    if (actionMessage) {
      tooltip.classList.remove("profile--copied");
      btnWrapper.classList.remove("profile--success");
      icon.className = "fi fi-rr-clipboard";
    }
  }, 2000);

  if (actionMessage) {
    btnWrapper.classList.add("profile--success");
    tooltip.classList.add("profile--copied");
  }

  navigator.clipboard.writeText(apiToken.innerText);
}

(function () {
  let loaded = false;
  let activePage = "";

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
  const historyLink = document.querySelector("#profile-history");

  if (accountLink)
    accountLink.addEventListener("click", handleClick(profileSpa, "account"));

  if (tokenLink)
    tokenLink.addEventListener("click", handleClick(profileSpa, "token"));

  if (historyLink)
    historyLink.addEventListener("click", handleClick(profileSpa, "history"));

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

        if (page === "account") {
          accountLink.classList.add("profile--active");
        } else if (page === "token") {
          tokenLink.classList.add("profile--active");
        } else {
          historyLink.classList.add("profile--active");
        }
      }
    };

    xhr.send();
  }
})();
