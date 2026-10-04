// Page behavior for Math Homework Helper, written without any framework.
(() => {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const body = document.body;
  const strings = JSON.parse((document.getElementById("i18n") || {}).textContent || "{}");

  // Translate a string and fill in named values.
  function t(text, values = {}) {
    return Object.entries(values).reduce((result, [key, value]) => result.replace(`{${key}}`, value), strings[text] || text);
  }

  const svg = (name) => `<svg class="icon" aria-hidden="true"><use href="#i-${name}"></use></svg>`;

  // Render LaTeX with KaTeX inside every top level .tex element.
  function renderMath(root = document) {
    if (!window.renderMathInElement) return;
    const scope = root.classList && root.classList.contains("tex") ? [root] : $$(".tex", root);
    scope
      .filter((el) => !el.parentElement || !el.parentElement.closest(".tex"))
      .forEach((el) =>
        window.renderMathInElement(el, {
          delimiters: [
            { left: "$$", right: "$$", display: true },
            { left: "\\[", right: "\\]", display: true },
            { left: "$", right: "$", display: false },
            { left: "\\(", right: "\\)", display: false },
          ],
          throwOnError: false,
        })
      );
  }

  // Send JSON with the CSRF token and return the parsed reply.
  async function postJSON(url, data = {}) {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json", "X-CSRFToken": body.dataset.csrf },
      body: JSON.stringify(data),
    });
    let reply = {};
    try {
      reply = await response.json();
    } catch {
      reply = {};
    }
    if (!response.ok) throw new Error(reply.error || t("Something went wrong. Please try again."));
    return reply;
  }

  // Show a short message in the corner of the screen.
  function toast(message, kind = "info") {
    const icons = { success: "check-circle", error: "alert", info: "info" };
    const item = document.createElement("div");
    item.className = `toast toast-${kind}`;
    item.setAttribute("role", "status");
    item.innerHTML = `${svg(icons[kind] || "info")}<p></p><button type="button" data-dismiss aria-label="${t("Dismiss")}">${svg("x")}</button>`;
    item.querySelector("p").textContent = message;
    $(".toasts").append(item);
    setTimeout(() => dismiss(item), 5000);
  }

  function dismiss(item) {
    if (!item || item.classList.contains("is-leaving")) return;
    item.classList.add("is-leaving");
    setTimeout(() => item.remove(), 250);
  }

  // Play a small tone for right and wrong answers when sounds are on.
  let audio;
  function sound(kind) {
    if (body.dataset.sounds !== "on") return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      const notes = kind === "good" ? [660, 880] : [320, 230];
      notes.forEach((frequency, i) => {
        const osc = audio.createOscillator();
        const gain = audio.createGain();
        const start = audio.currentTime + i * 0.12;
        osc.type = kind === "good" ? "sine" : "triangle";
        osc.frequency.value = frequency;
        gain.gain.setValueAtTime(0.0001, start);
        gain.gain.exponentialRampToValueAtTime(0.16, start + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.0001, start + 0.2);
        osc.connect(gain).connect(audio.destination);
        osc.start(start);
        osc.stop(start + 0.22);
      });
    } catch {
      // Audio is optional, so a failure here is ignored.
    }
  }

  // Mascot: Beral with a speech bubble, shown after real events. Beral is a rigged 3D character when a model is
  // installed and the device can draw it, and one of the four pictures otherwise.
  function createMascot() {
    const root = $("[data-mascot]");
    const source = $("#mascot-data");
    const data = source ? JSON.parse(source.textContent) : null;
    const none = () => Promise.resolve(false);
    if (!root || !data) return { show: none, say: none, play: none, think() {}, hide() {} };
    const image = $("[data-mascot-img]", root);
    const stage = $("[data-mascot-stage]", root);
    const bubble = $(".mascot-bubble", root);
    const text = $("[data-mascot-text]", root);
    const live = $("[data-mascot-live]");
    const important = "button, .btn, input, select, textarea, .choice, .chip, .segmented, .dropzone, .keypad, .answer, .working, .feedback, .composer, .tabbar, .topbar, .sidebar, .problem-text, .step-result, .question, .katex";
    const touch = () => window.matchMedia("(max-width: 1024px)").matches;
    const still = window.matchMedia("(prefers-reduced-motion: reduce)");
    const POSE = { welcome: "welcome", success: "celebrate", celebrate: "celebrate", encourage: "encourage", thinking: "thinking" };
    let timer;
    let visible = false;
    let character = null;
    let docked = false;
    let holding = false;
    let restingAt = 0;
    let host = null;
    let waitingThink = null;

    // Find the lowest corner spot that covers no control, answer box or navigation.
    function findSpot() {
      const box = root.getBoundingClientRect();
      const edge = touch() ? 12 : 24;
      const taken = $$(important)
        .filter((el) => !root.contains(el))
        .map((el) => el.getBoundingClientRect())
        .filter((r) => r.width && r.height && r.bottom > 0 && r.top < window.innerHeight);
      const free = (left, top) => !taken.some((r) => left < r.right && left + box.width > r.left && top < r.bottom && top + box.height > r.top);
      for (let bottom = edge; bottom + box.height <= window.innerHeight * 0.8; bottom += 12) {
        for (const side of touch() ? ["left", "right"] : ["right"]) {
          const left = side === "left" ? edge : window.innerWidth - edge - box.width;
          if (free(left, window.innerHeight - bottom - box.height)) return { side, bottom, edge };
        }
      }
      return null;
    }

    // On wide screens Beral uses the empty margin beside the page, where the 3D Beral can also stay between events.
    function dockSpot() {
      const page = $(".page");
      if (touch() || !page) return null;
      const contentRight = Math.max(0, ...[...page.children].map((el) => el.getBoundingClientRect().right));
      const gutter = window.innerWidth - contentRight;
      const width = character ? parseFloat(getComputedStyle(stage).width) || 170 : image.offsetWidth || 120;
      return gutter >= width + 22 ? { gutter } : null;
    }

    function place() {
      const dock = dockSpot();
      docked = Boolean(dock);
      root.dataset.layout = docked ? "dock" : "pop";
      if (docked) {
        root.style.left = "auto";
        root.style.right = "10px";
        root.style.bottom = "16px";
        root.style.width = `${dock.gutter - 20}px`;
        return true;
      }
      root.style.width = "";
      root.dataset.side = touch() ? "left" : "right";
      let spot = findSpot();
      if (spot && spot.side !== root.dataset.side) {
        root.dataset.side = spot.side;
        spot = findSpot();
      }
      if (!spot) return false;
      root.style.bottom = `${spot.bottom}px`;
      root.style.left = spot.side === "left" ? `${spot.edge}px` : "auto";
      root.style.right = spot.side === "right" ? `${spot.edge}px` : "auto";
      return true;
    }

    function hideBubble() {
      bubble.hidden = true;
      live.textContent = "";
    }

    // Hide the whole mascot, except a docked 3D Beral, which stays and only loses its bubble.
    function hide(force = false) {
      clearTimeout(timer);
      if (!visible) return;
      if (docked && character && !force) return hideBubble();
      visible = false;
      root.classList.remove("is-open");
      live.textContent = "";
      setTimeout(() => {
        if (visible) return;
        root.hidden = true;
        if (character && !host) character.setActive(false);
      }, 320);
    }

    // A popped up 3D Beral leaves once the bubble has been read and the animation is back at rest.
    function leaveWhenDone(until) {
      clearTimeout(timer);
      const wait = () => {
        if (holding) return;
        if (character && !/^(idle|thinking)$/.test(character.state || "idle")) return (timer = setTimeout(wait, 250));
        timer = setTimeout(hide, Math.max(until - Date.now(), Date.now() - restingAt < 700 ? 700 : 0));
      };
      timer = setTimeout(wait, Math.max(until - Date.now(), 0));
    }

    // Show Beral with an animation and an optional message; resolves to false when there is no free spot.
    function show({ state, animation, message = "", duration = data.duration }) {
      animation = animation || Object.keys(POSE).find((key) => POSE[key] === state) || "welcome";
      const pose = state || POSE[animation] || "welcome";
      if ((!character && animation === "idle") || host) return Promise.resolve(false);
      clearTimeout(timer);
      visible = true;
      return new Promise((resolve) => {
        const reveal = () => {
          if (!visible) return resolve(false);
          text.textContent = message;
          bubble.hidden = !message;
          root.dataset.state = pose;
          root.hidden = false;
          if (!place()) {
            visible = false;
            root.classList.remove("is-open");
            root.hidden = true;
            return resolve(false);
          }
          requestAnimationFrame(() => root.classList.add("is-open"));
          if (message) live.textContent = message;
          if (character) {
            character.setActive(true);
            if (!character.play(animation)) restingAt = Date.now();
            if (docked) timer = setTimeout(hideBubble, duration);
            else leaveWhenDone(Date.now() + (message ? duration : 0));
          } else {
            timer = setTimeout(hide, duration);
          }
          resolve(true);
        };
        if (character) return reveal();
        const url = data.images[pose] || data.images.welcome;
        if (image.getAttribute("src") === url && image.complete) return reveal();
        image.onload = image.onerror = reveal;
        image.src = url;
      });
    }

    function say(key, options = {}) {
      const entry = data.messages[key];
      return entry ? show({ state: entry.state, animation: entry.animation, message: entry.text, ...options }) : Promise.resolve(false);
    }

    // Thinking while the app works: inside a given box such as the loading card, or in Beral's usual place.
    function think(on, box = null) {
      if (!character) {
        waitingThink = on ? { box } : null;
        return;
      }
      if (on) {
        holding = true;
        if (box) {
          host = box;
          box.classList.add("has-mascot");
          box.prepend(stage);
          character.setActive(true);
          character.play("thinking") || character.play("idle");
        } else {
          show({ animation: "thinking" });
        }
        return;
      }
      holding = false;
      if (host) {
        host.classList.remove("has-mascot");
        root.append(stage);
        host = null;
      }
      character.play("idle");
      restingAt = Date.now();
      if (visible && !docked) leaveWhenDone(Date.now() + 600);
      else if (!visible) character.setActive(false);
    }

    function fallBack(error) {
      if (error) console.warn("Beral 3D is not available, so the picture is used instead.", error);
      if (character) character.dispose();
      character = null;
      delete root.dataset.render;
      delete root.dataset.layout;
      hide(true);
    }

    // Load the 3D Beral after the page is ready, only when a model exists and the device can draw it well.
    function canDraw3D() {
      if (!data.three || still.matches || !(HTMLScriptElement.supports && HTMLScriptElement.supports("importmap"))) return false;
      const connection = navigator.connection;
      if ((connection && connection.saveData) || (navigator.deviceMemory && navigator.deviceMemory < 2)) return false;
      try {
        const probe = document.createElement("canvas");
        return Boolean(probe.getContext("webgl2") || probe.getContext("webgl"));
      } catch {
        return false;
      }
    }
    const ready = new Promise((resolve) => {
      if (!canDraw3D()) return resolve(false);
      const load = () =>
        import(data.three.module)
          .then(({ createBeral }) =>
            createBeral({
              container: stage, modelUrl: data.three.model, decoderPath: data.three.decoders,
              maxPixelRatio: touch() ? 1.5 : 1.75, onLost: () => fallBack(new Error("The graphics context was lost.")),
              onState: (name) => {
                root.dataset.animation = name;
                if (name === "idle" || name === "thinking") restingAt = Date.now();
              },
            })
          )
          .then((controller) => {
            character = controller;
            character.setActive(false);
            root.dataset.render = "3d";
            resolve(true);
            if (waitingThink) think(true, waitingThink.box);
            waitingThink = null;
          })
          .catch((error) => {
            fallBack(error);
            resolve(false);
          });
      const soon = window.requestIdleCallback || ((callback) => setTimeout(callback, 200));
      const start = () => soon(load, { timeout: 800 });
      if (document.readyState === "complete") start();
      else window.addEventListener("load", start, { once: true });
    });
    still.addEventListener("change", () => still.matches && character && fallBack());
    window.addEventListener("resize", () => {
      if (character && visible && !host && !holding) {
        const wasDocked = docked;
        if (!place() || wasDocked !== docked) hide(true);
      }
    });

    const dismiss = () => (docked && character ? hideBubble() : hide());
    $("[data-mascot-close]", root).addEventListener("click", dismiss);
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && visible) dismiss();
    });

    // Greet once per browsing session, or speak about what just happened on the server.
    const read = (store, key) => {
      try {
        return Boolean(store.getItem(key));
      } catch {
        return false;
      }
    };
    const mark = (store, key) => {
      try {
        store.setItem(key, "1");
      } catch {
        // Storage can be unavailable, in which case the mascot simply greets again.
      }
    };
    const settled = Promise.race([ready, new Promise((resolve) => setTimeout(resolve, 6000))]);
    if (data.event) {
      if (data.welcome) mark(sessionStorage, "mascot.welcomed");
      settled.then(() => setTimeout(() => say(data.event), 300));
    } else if (data.welcome && !read(sessionStorage, "mascot.welcomed")) {
      settled.then(() =>
        setTimeout(async () => {
          const shown = await say(read(localStorage, "mascot.known") ? "welcome_back" : "welcome");
          if (!shown) return;
          mark(sessionStorage, "mascot.welcomed");
          mark(localStorage, "mascot.known");
        }, 400)
      );
    }

    // On wide screens a ready 3D Beral stays in the margin and idles quietly between events.
    if (data.welcome) {
      ready.then((ok) => ok && setTimeout(() => !visible && dockSpot() && show({ animation: "idle" }), 1500));
    }

    // A small API for the rest of the app and for testing: beral.play("celebrate"), beral.think(true).
    const api = {
      show, say, hide, think, ready,
      play: (name) => show({ animation: name }),
      get mode() {
        return character ? "3d" : "picture";
      },
      get character() {
        return character;
      },
    };
    window.beral = api;
    return api;
  }

  // Insert text at the cursor inside a textarea.
  function insertAtCursor(field, text) {
    field.focus();
    field.setRangeText(text, field.selectionStart, field.selectionEnd, "end");
    field.dispatchEvent(new Event("input"));
  }

  // Grow a textarea with its content up to its max height.
  function autoGrow(field) {
    field.style.height = "auto";
    field.style.height = `${Math.min(field.scrollHeight + 2, 160)}px`;
  }

  // Shared behavior found on many pages.
  function initCommon() {
    $$(".toast").forEach((item) => setTimeout(() => dismiss(item), 5000));
    document.addEventListener("click", (event) => {
      const button = event.target.closest("[data-dismiss]");
      if (button) dismiss(button.closest(".toast"));
    });

    document.addEventListener("submit", (event) => {
      const message = event.target.dataset.confirm;
      if (message && !window.confirm(message)) event.preventDefault();
    });

    $$("[data-reveal]").forEach((button) =>
      button.addEventListener("click", () => {
        const input = document.getElementById(button.dataset.reveal);
        const show = input.type === "password";
        input.type = show ? "text" : "password";
        button.querySelector("use").setAttribute("href", show ? "#i-eye-off" : "#i-eye");
        button.setAttribute("aria-label", show ? t("Hide password") : t("Show password"));
      })
    );

    const zone = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    $$("[data-timezone-field]").forEach((field) => (field.value = zone));
    if (body.dataset.timezoneUrl && zone && body.dataset.timezone !== zone) {
      postJSON(body.dataset.timezoneUrl, { timezone: zone }).catch(() => {});
    }

    const menu = $("[data-menu]");
    if (menu) {
      document.addEventListener("click", (event) => {
        if (menu.open && !menu.contains(event.target)) menu.open = false;
      });
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") menu.open = false;
      });
    }

    $$('input[name="theme"]').forEach((radio) =>
      radio.addEventListener("change", () => (document.documentElement.dataset.theme = radio.value))
    );
  }

  // Solve page: tabs, photo picking, symbol keypad and the loading screen.
  function initSolve() {
    const form = $("[data-solve-form]");
    if (!form) return;
    const modeField = $("[data-mode-field]", form);
    const photoInput = $("[data-photo-input]", form);
    const cameraInput = $("[data-camera-input]", form);
    const dropzone = $("[data-dropzone]", form);
    const preview = $("[data-preview]", form);
    const problem = $("[data-problem]", form);

    function setMode(mode) {
      modeField.value = mode;
      $$("[data-mode]", form).forEach((tab) => {
        tab.classList.toggle("is-active", tab.dataset.mode === mode);
        tab.setAttribute("aria-selected", String(tab.dataset.mode === mode));
      });
      $$("[data-panel]", form).forEach((panel) => (panel.hidden = panel.dataset.panel !== mode));
      history.replaceState(null, "", mode === "type" ? "?mode=type" : location.pathname);
      if (mode === "type") problem.focus();
    }
    $$("[data-mode]", form).forEach((tab) => tab.addEventListener("click", () => setMode(tab.dataset.mode)));

    // Shrink large photos in the browser so uploads are quick and fit host limits.
    async function shrink(file) {
      try {
        const bitmap = await createImageBitmap(file, { imageOrientation: "from-image" });
        const scale = Math.min(1, 1600 / Math.max(bitmap.width, bitmap.height));
        if (scale === 1 && file.size < 1024 * 1024) return file;
        const canvas = document.createElement("canvas");
        canvas.width = Math.round(bitmap.width * scale);
        canvas.height = Math.round(bitmap.height * scale);
        const context = canvas.getContext("2d");
        context.fillStyle = "#fff";
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
        const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", 0.85));
        const name = `${(file.name || "photo").replace(/\.\w+$/, "")}.jpg`;
        return blob ? new File([blob], name, { type: "image/jpeg" }) : file;
      } catch {
        return file;
      }
    }

    async function useFile(original) {
      if (!original) return;
      if (!original.type.startsWith("image/")) return toast(t("Please choose an image file."), "error");
      if (original.size > 12 * 1024 * 1024) return toast(t("That photo is over 12 MB. Please use a smaller one."), "error");
      const file = await shrink(original);
      if (file.size > 4 * 1024 * 1024) return toast(t("That photo is too large to upload. Please crop it and try again."), "error");
      const transfer = new DataTransfer();
      transfer.items.add(file);
      photoInput.files = transfer.files;
      $("[data-preview-img]", form).src = URL.createObjectURL(file);
      $("[data-file-name]", form).textContent = file.name || t("Pasted image");
      dropzone.hidden = true;
      preview.hidden = false;
    }

    photoInput.addEventListener("change", () => useFile(photoInput.files[0]));
    cameraInput.addEventListener("change", () => useFile(cameraInput.files[0]));
    $("[data-open-files]", form).addEventListener("click", (event) => {
      event.stopPropagation();
      photoInput.click();
    });
    $("[data-open-camera]", form).addEventListener("click", (event) => {
      event.stopPropagation();
      cameraInput.click();
    });
    dropzone.addEventListener("click", () => photoInput.click());
    dropzone.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        photoInput.click();
      }
    });
    ["dragenter", "dragover"].forEach((name) =>
      dropzone.addEventListener(name, (event) => {
        event.preventDefault();
        dropzone.classList.add("is-over");
      })
    );
    ["dragleave", "drop"].forEach((name) =>
      dropzone.addEventListener(name, (event) => {
        event.preventDefault();
        dropzone.classList.remove("is-over");
      })
    );
    dropzone.addEventListener("drop", (event) => useFile(event.dataTransfer.files[0]));
    document.addEventListener("paste", (event) => {
      const item = [...(event.clipboardData?.items || [])].find((entry) => entry.type.startsWith("image/"));
      if (!item) return;
      setMode("photo");
      useFile(item.getAsFile());
    });
    $("[data-clear-photo]", form).addEventListener("click", () => {
      photoInput.value = "";
      preview.hidden = true;
      dropzone.hidden = false;
    });

    $$("[data-insert]", form).forEach((key) => key.addEventListener("click", () => insertAtCursor(problem, key.dataset.insert)));
    $$("[data-example]", form).forEach((chip) =>
      chip.addEventListener("click", () => {
        problem.value = chip.dataset.example;
        problem.focus();
      })
    );

    const overlay = $("[data-loading]");
    const status = $("[data-loading-text]");
    const messages = ["Reading your problem", "Working through each step", "Double checking the math", "Writing up the explanation"].map((text) => t(text));
    let timer;
    form.addEventListener("submit", (event) => {
      const mode = modeField.value;
      if (mode === "photo" && !photoInput.files.length) {
        event.preventDefault();
        return toast(t("Choose or take a photo first."), "error");
      }
      if (mode === "type" && problem.value.trim().length < 2) {
        event.preventDefault();
        problem.focus();
        return toast(t("Type the problem you want solved."), "error");
      }
      photoInput.disabled = mode !== "photo";
      let step = 0;
      status.textContent = messages[0];
      overlay.hidden = false;
      mascot.think(true, $(".card", overlay));
      timer = setInterval(() => (status.textContent = messages[++step % messages.length]), 2600);
    });
    window.addEventListener("pageshow", () => {
      clearInterval(timer);
      overlay.hidden = true;
      mascot.think(false);
      photoInput.disabled = false;
    });
  }

  // Solution page: step reveal, saving and the tutor chat.
  function initSolution() {
    $$("[data-problem]").forEach((card) => {
      const steps = $$(".step", card);
      const next = $("[data-next-step]", card);
      if (!next) return;
      const hidden = () => steps.filter((step) => step.classList.contains("is-hidden"));
      const reveal = (step) => {
        step.classList.remove("is-hidden");
        const line = $(`[data-step-line="${steps.indexOf(step)}"]`, card);
        if (line) line.classList.remove("is-hidden");
      };
      const update = () => {
        const left = hidden().length;
        if (!left) $("[data-step-controls]", card).hidden = true;
        else $("span", next).textContent = left === steps.length ? t("Show the first step") : t("Show the next step ({left} left)", { left });
      };
      next.addEventListener("click", () => {
        const step = hidden()[0];
        if (step) reveal(step);
        update();
      });
      $("[data-all-steps]", card).addEventListener("click", () => {
        steps.forEach(reveal);
        update();
      });
    });

    const starForm = $("[data-star-form]");
    if (starForm) {
      starForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
          const { starred } = await postJSON(starForm.action);
          const button = $("button", starForm);
          button.classList.toggle("is-starred", starred);
          $("span", button).textContent = starred ? t("Saved") : t("Save");
          if (starred) mascot.say("saved");
          else toast(t("Removed from saved."), "success");
        } catch (error) {
          toast(error.message, "error");
        }
      });
    }

    const askForm = $("[data-ask-form]");
    if (!askForm) return;
    const input = $("[data-question]", askForm);
    const send = $("button", askForm);
    const chat = $("[data-chat]");
    const suggestions = $("[data-suggestions]");

    async function ask(text) {
      const question = text.trim();
      if (!question || send.disabled) return;
      input.value = "";
      autoGrow(input);
      send.disabled = true;
      suggestions.hidden = true;

      const mine = document.createElement("div");
      mine.className = "bubble-row user";
      mine.innerHTML = '<div class="msg user"></div>';
      mine.firstChild.textContent = question;
      const pending = document.createElement("div");
      pending.className = "bubble-row";
      pending.innerHTML = `<span class="tutor-avatar">${svg("sparkles")}</span><div class="msg assistant"><span class="muted">${t("Thinking")}</span><span class="dots"></span></div>`;
      chat.append(mine, pending);
      pending.scrollIntoView({ behavior: "smooth", block: "nearest" });

      mascot.think(true);
      try {
        const { html } = await postJSON(askForm.action, { question });
        mine.remove();
        pending.remove();
        const holder = document.createElement("div");
        holder.innerHTML = html;
        const added = [...holder.children];
        chat.append(...added);
        renderMath(chat);
        added[added.length - 1].scrollIntoView({ behavior: "smooth", block: "nearest" });
      } catch (error) {
        mine.remove();
        pending.remove();
        input.value = question;
        if (!chat.children.length) suggestions.hidden = false;
        toast(error.message, "error");
      } finally {
        mascot.think(false);
        send.disabled = false;
        input.focus();
      }
    }

    askForm.addEventListener("submit", (event) => {
      event.preventDefault();
      ask(input.value);
    });
    input.addEventListener("input", () => autoGrow(input));
    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        ask(input.value);
      }
    });
    $$("[data-prompt]").forEach((chip) => chip.addEventListener("click", () => ask(chip.dataset.prompt)));
  }

  // Practice round: one question at a time with instant feedback.
  function initQuiz() {
    const root = $("[data-quiz]");
    if (!root) return;
    const questions = JSON.parse($("#quiz-data").textContent);
    const answers = [];
    const prompt = $("[data-question]", root);
    const choices = $("[data-choices]", root);
    const feedback = $("[data-feedback]", root);
    const next = $("[data-next]", root);
    const bar = $("[data-progress]", root);
    const count = $("[data-count]", root);
    const form = $("[data-finish-form]", root);
    let index = 0;
    let locked = false;
    let streak = 0;
    let misses = 0;
    let cheered = false;

    // The mascot reacts to real answers, but only now and then, to avoid distracting.
    function react(good) {
      if (good) {
        streak += 1;
        if (!cheered) mascot.say("correct");
        else if (streak % 3 === 0) mascot.say("encourage");
        cheered = true;
      } else {
        streak = 0;
        misses += 1;
        if (misses === 1) mascot.say("wrong");
        else if (misses === 3) mascot.say("reminder");
      }
    }

    function show() {
      const item = questions[index];
      locked = false;
      prompt.textContent = item.prompt;
      choices.innerHTML = "";
      item.choices.forEach((choice, i) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "choice";
        button.innerHTML = `<span class="key">${"ABCD"[i]}</span><span class="text"></span>`;
        $(".text", button).textContent = choice;
        button.addEventListener("click", () => choose(i));
        choices.append(button);
      });
      feedback.hidden = true;
      next.hidden = true;
      bar.style.width = `${(index / questions.length) * 100}%`;
      count.textContent = `${index + 1} / ${questions.length}`;
      renderMath(root);
    }

    function choose(pick) {
      if (locked) return;
      locked = true;
      answers[index] = pick;
      const item = questions[index];
      const good = pick === item.answer;
      $$(".choice", choices).forEach((button, i) => {
        button.disabled = true;
        if (i === item.answer) button.classList.add("is-correct");
        else if (i === pick) button.classList.add("is-wrong");
      });
      feedback.className = `feedback tex ${good ? "good" : "bad"}`;
      feedback.innerHTML = `<h3>${svg(good ? "check-circle" : "alert")}${good ? t("Correct!") : t("Not quite")}</h3><p></p>`;
      $("p", feedback).textContent = item.explanation;
      feedback.hidden = false;
      $("span", next).textContent = index === questions.length - 1 ? t("See results") : t("Next");
      next.hidden = false;
      bar.style.width = `${((index + 1) / questions.length) * 100}%`;
      renderMath(feedback);
      sound(good ? "good" : "bad");
      next.focus({ preventScroll: true });
      feedback.scrollIntoView({ behavior: "smooth", block: "nearest" });
      next.scrollIntoView({ behavior: "smooth", block: "nearest" });
      const answered = index;
      setTimeout(() => {
        if (locked && index === answered) react(good);
      }, 550);
    }

    function finish() {
      form.elements.answers.value = questions.map((_, i) => (answers[i] ?? -1)).join(",");
      next.disabled = true;
      form.submit();
    }

    next.addEventListener("click", () => {
      mascot.hide();
      if (index < questions.length - 1) {
        index += 1;
        show();
        window.scrollTo({ top: 0, behavior: "smooth" });
      } else {
        finish();
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.target.matches("input, textarea, select") || event.metaKey || event.ctrlKey || event.altKey) return;
      const position = ["1", "2", "3", "4"].indexOf(event.key);
      if (!locked && position >= 0 && position < questions[index].choices.length) choose(position);
      else if (locked && event.key === "Enter" && document.activeElement !== next) {
        event.preventDefault();
        next.click();
      }
    });

    $("[data-quit]", root).addEventListener("click", (event) => {
      if (answers.length && !window.confirm(t("Leave this round? Your answers so far will not be saved."))) event.preventDefault();
    });

    show();
  }

  // Admin practice editor: add and remove question blocks.
  function initQuestionEditor() {
    const list = $("[data-questions]");
    const template = $("[data-question-template]");
    if (!list || !template) return;
    let next = Number(list.dataset.nextIndex) || 0;
    const renumber = () => $$("[data-question-number]", list).forEach((label, i) => (label.textContent = i + 1));
    $("[data-add-question]").addEventListener("click", () => {
      const html = template.innerHTML.replaceAll("__index__", String(next));
      next += 1;
      list.insertAdjacentHTML("beforeend", html);
      renumber();
      const added = list.lastElementChild;
      added.scrollIntoView({ behavior: "smooth", block: "center" });
      $("textarea", added).focus({ preventScroll: true });
    });
    list.addEventListener("click", (event) => {
      const button = event.target.closest("[data-remove-question]");
      if (!button) return;
      button.closest("[data-question]").remove();
      renumber();
    });
  }

  const mascot = createMascot();
  initCommon();
  renderMath();
  initSolve();
  initSolution();
  initQuiz();
  initQuestionEditor();
})();
