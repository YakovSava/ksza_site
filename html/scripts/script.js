var button = document.querySelectorAll(".dropdown__button");
let intervalId;

button.forEach(e => {
  e.addEventListener('click', e => {
    const menu = e.currentTarget.dataset.path;
    document.querySelectorAll(".dropdown__content").forEach(e => {
      if (!document.querySelector(`[data-target=${menu}]`).classList.contains("openM")) {
        e.classList.remove("openM");
        e.classList.remove("open");
        document.querySelector(`[data-target=${menu}]`).classList.add("open")
        intervalId = setTimeout(() => {
          document.querySelector(`[data-target=${menu}]`).classList.add("openM");
        }, 0);
      }

      if (document.querySelector(`[data-target=${menu}]`).classList.contains("openM")) {
        clearTimeout(intervalId);
        document.querySelector(`[data-target=${menu}]`).classList.remove("open");
        intervalId = setTimeout(() => {
          document.querySelector(`[data-target=${menu}]`).classList.remove("openM");
        }, 0);
      }
      window.onclick = e => {
        if(e.target == document.querySelector(`[data-target=${menu}]`) || e.target == document.querySelector(`[data-path=${menu}]`)) {
          return;
        } else {
          document.querySelector(`[data-target=${menu}]`).classList.remove("open");
          document.querySelector(`[data-target=${menu}]`).classList.remove("openM");
        }
      }
    });
  });
});