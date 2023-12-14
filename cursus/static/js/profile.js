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

  const updateUri = encodeURI(`/profile/update_name/${value}`);

  fetch(updateUri, {
    method: "PUT",
    headers: {
      Accept: "application/json",
    },
  })
    .then((res) => {
      return res.json();
    })
    .then(({ type, message, data }) => {
      const profileFullName = document.querySelector(".profile__fullname");
      const feedbackElement = document.querySelector(
        `.profile__field__input-feedback[for="${input.getAttribute("id")}"]`
      );
      const resetBtn = document.getElementById(
        input.getAttribute("data-cursus-reset-by")
      );
      const submitBtn = document.getElementById(
        input.getAttribute("data-cursus-submit-by")
      );

      if (!feedbackElement) {
        throw new Error("Feedback element not found");
      }

      if (type === "success") {
        feedbackElement.classList.remove("error");
        feedbackElement.classList.add("success", "show");
        feedbackElement.innerText = message;

        input.setAttribute("data-cursus-init-value", data.name);
        input.value = data.name;
        input.title = data.name;

        resetBtn.classList.add("display-none");

        submitBtn.classList.add("btn--secondary");
        submitBtn.classList.remove("btn--primary");

        profileFullName.innerText = data.name;
      } else {
        feedbackElement.classList.remove("success");
        feedbackElement.classList.add("error", "show");
        feedbackElement.innerText = message;
        feedbackElement.title = message;
      }
    })
    .catch((err) => {
      console.error(err);
    });
}

let isModalOpen = false;

/**
 * @param {MouseEvent} e
 */
function handleOpenModal(e) {
  e.preventDefault();

  const modal = document.getElementById("modal");

  modal.classList.add("modal--open");
}

/**
 * @param {MouseEvent} e
 */
function handleDeleteAccount(e) {
  e.preventDefault();

  console.log("delete account");
}

/**
 *
 * @param {MouseEvent} e
 */
function handleCloseModal(e) {
  e.preventDefault();

  const modal = document.getElementById("modal");

  modal.classList.remove("modal--open");
}

function _mountAccount() {
  document.title = "Account - Profile - Cursus";

  const displayNameCancelBtn = document.getElementById(
    "profile-display-cancel-name-btn"
  );

  const displayNameSubmitBtn = document.getElementById(
    "profile-display-submit-name-btn"
  );

  const deleteAccountBtn = document.getElementById(
    "profile-delete-account-btn"
  );

  const modal = document.getElementById("modal");

  if (displayNameCancelBtn)
    displayNameCancelBtn.addEventListener("click", handleCancelDisplayName);

  if (displayNameSubmitBtn)
    displayNameSubmitBtn.addEventListener("click", handleUpdateDisplayName);

  if (deleteAccountBtn)
    deleteAccountBtn.addEventListener("click", handleOpenModal);

  if (modal) {
    modal.innerHTML = `
<div class="profile__modal">
  <div class="profile__modal__header">
    <h1>Warning</h1>
    <button id="close-modal-btn" class="btn btn--icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M5.72 5.72a.75.75 0 0 1 1.06 0L12 10.94l5.22-5.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L13.06 12l5.22 5.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L12 13.06l-5.22 5.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L10.94 12 5.72 6.78a.75.75 0 0 1 0-1.06Z"></path></svg>
    </button>
  </div>
  <div class="profile__modal__content">
    <p>
      Are you sure you want to delete your account? This action is irreversible.
    </p>
    <div class="profile__modal__footer">
      <button id="cancel-delete-btn" class="btn btn--secondary">
        Cancel
      </button>
      <button id="actual-delete-btn" class="btn btn--primary btn--danger">
        I&apos;m sure
      </button>
    </div>
  </div>
</div>`;
  }

  const actualDeleteBtn = document.getElementById("actual-delete-btn");
  const cancelDeleleteBtn = document.getElementById("cancel-delete-btn");
  const closeModalBtn = document.getElementById("close-modal-btn");

  if (actualDeleteBtn)
    actualDeleteBtn.addEventListener("click", handleDeleteAccount);

  if (cancelDeleleteBtn && closeModalBtn) {
    cancelDeleleteBtn.addEventListener("click", handleCloseModal);
    closeModalBtn.addEventListener("click", handleCloseModal);
  }

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
