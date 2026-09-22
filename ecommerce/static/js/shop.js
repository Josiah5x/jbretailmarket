// document.addEventListener("DOMContentLoaded", function () {
//   console.log("MiniStore initialized");
// });


// document.addEventListener("DOMContentLoaded", function () {
//   const quickViewModal = document.getElementById("quickViewModal");

//   const quickViewLoading = document.getElementById("quickViewLoading");

//   const quickViewContent = document.getElementById("quickViewContent");

//   document.querySelectorAll(".quick-view-btn").forEach(function (button) {
//     button.addEventListener("click", async function () {
//       const url = this.dataset.productUrl;

//       quickViewLoading.classList.remove("d-none");

//       quickViewContent.innerHTML = "";

//       try {
//         const response = await fetch(url, {
//           headers: {
//             "X-Requested-With": "XMLHttpRequest",
//           },
//         });

//         if (!response.ok) {
//           throw new Error("Unable to load product.");
//         }

//         const html = await response.text();

//         quickViewContent.innerHTML = html;
//       } catch (error) {
//         quickViewContent.innerHTML = `
//                             <div class="alert alert-danger">
//                                 Unable to load product details.
//                             </div>
//                         `;

//         console.error(error);
//       } finally {
//         quickViewLoading.classList.add("d-none");
//       }
//     });
//   });
// });



document.addEventListener("DOMContentLoaded", function () {
  /*
    =========================================
    CSRF
    =========================================
    */

  function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");

      for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

          break;
        }
      }
    }

    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  /*
    =========================================
    UPDATE CART COUNT
    =========================================
    */

  function updateCartCount(count) {
    document.querySelectorAll(".cart-count").forEach(function (element) {
      element.textContent = count;
    });
  }

  /*
    =========================================
    ADD TO CART
    =========================================
    */

  document.querySelectorAll(".add-to-cart").forEach(function (button) {
    button.addEventListener("click", async function () {
      const url = this.dataset.addUrl;

      if (!url) {
        console.error("Cart URL missing.");
        return;
      }

      const originalHTML = this.innerHTML;

      this.disabled = true;

      this.innerHTML = `
                        <span
                            class="spinner-border spinner-border-sm me-1"
                        ></span>
                        Adding...
                    `;

      try {
        const response = await fetch(url, {
          method: "POST",

          headers: {
            "X-CSRFToken": csrftoken,

            "X-Requested-With": "XMLHttpRequest",
          },
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || "Unable to add product.");
        }

        updateCartCount(data.item_count);

        this.innerHTML = `
                            <i class="bi bi-check-lg me-1"></i>
                            Added
                        `;

        showCartMessage(data.message, "success");

        setTimeout(() => {
          this.innerHTML = originalHTML;

          this.disabled = false;
        }, 1500);
      } catch (error) {
        this.innerHTML = originalHTML;

        this.disabled = false;

        showCartMessage(error.message, "danger");
      }
    });
  });

  /*
    =========================================
    CART MESSAGE
    =========================================
    */

  function showCartMessage(message, type = "success") {
    let container = document.getElementById("cartMessageContainer");

    if (!container) {
      container = document.createElement("div");

      container.id = "cartMessageContainer";

      container.className = "position-fixed top-0 end-0 p-3";

      container.style.zIndex = "9999";

      document.body.appendChild(container);
    }

    const alert = document.createElement("div");

    alert.className = `alert alert-${type} shadow`;

    alert.innerHTML = `
            <i class="bi bi-cart-check me-2"></i>
            ${message}
        `;

    container.appendChild(alert);

    setTimeout(() => {
      alert.remove();
    }, 3000);
  }

  /*
    =========================================
    QUICK VIEW
    =========================================
    */

  const quickViewModal = document.getElementById("quickViewModal");

  const quickViewLoading = document.getElementById("quickViewLoading");

  const quickViewContent = document.getElementById("quickViewContent");

  if (quickViewModal && quickViewLoading && quickViewContent) {
    document.querySelectorAll(".quick-view-btn").forEach(function (button) {
      button.addEventListener("click", async function () {
        const url = this.dataset.productUrl;

        quickViewLoading.classList.remove("d-none");

        quickViewContent.innerHTML = "";

        try {
          const response = await fetch(url, {
            headers: {
              "X-Requested-With": "XMLHttpRequest",
            },
          });

          if (!response.ok) {
            throw new Error("Unable to load product.");
          }

          const html = await response.text();

          quickViewContent.innerHTML = html;

          /*
                            Re-bind Add to Cart
                            buttons loaded into
                            the modal.
                            */

          bindQuickViewCartButtons();
        } catch (error) {
          quickViewContent.innerHTML = `
                                <div class="alert alert-danger">
                                    Unable to load product details.
                                </div>
                            `;

          console.error(error);
        } finally {
          quickViewLoading.classList.add("d-none");
        }
      });
    });
  }

  /*
    =========================================
    QUICK VIEW CART BUTTON
    =========================================
    */

  function bindQuickViewCartButtons() {
    document
      .querySelectorAll("#quickViewContent .add-to-cart")
      .forEach(function (button) {
        button.addEventListener("click", async function () {
          const url = this.dataset.addUrl;

          if (!url) {
            return;
          }

          try {
            const response = await fetch(url, {
              method: "POST",

              headers: {
                "X-CSRFToken": csrftoken,

                "X-Requested-With": "XMLHttpRequest",
              },
            });

            const data = await response.json();

            if (!response.ok) {
              throw new Error(data.message);
            }

            updateCartCount(data.item_count);

            showCartMessage(data.message, "success");
          } catch (error) {
            showCartMessage(error.message, "danger");
          }
        });
      });
  }
});