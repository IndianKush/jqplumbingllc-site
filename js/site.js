/* ============================================================
   SITE SETTINGS.
   FORM_ENDPOINT: where estimate requests are emailed (FormSubmit).
   Google Analytics, Google Ads and conversion tracking are handled by
   Google Tag Manager (GTM-5SBR2GC4). Do not add Google tags to the site code.
   ============================================================ */
window.JQ_CONFIG = {
  /* After Jon activates FormSubmit, swap the email for the random alias FormSubmit
     sends him, to hide the address from spammers. */
  FORM_ENDPOINT: "https://formsubmit.co/ajax/Jonq@jqplumbingllc.com"
};

(function () {
  var C = window.JQ_CONFIG;
  window.dataLayer = window.dataLayer || [];

  /* Pushes a named event to the dataLayer (read by Google Tag Manager).
     No Google tags are called from here. */
  function track(name, params) {
    var payload = { event: name };
    for (var k in (params || {})) payload[k] = params[k];
    dataLayer.push(payload);
  }
  window.jqTrack = track;

  /* Click to call: every tel: link on the site */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"]');
    if (!a || a.hasAttribute("data-no-track")) return;
    track("call_click", {
      link_location: a.getAttribute("data-call-location") || "other",
      page_path: location.pathname
    });
  });

  /* Estimate form: validates, posts to FormSubmit, fires generate_lead only on success */
  document.querySelectorAll("form.form").forEach(function (form) {
    var status = form.querySelector(".form-status");
    var pageField = form.querySelector('input[name="page"]');
    if (pageField) pageField.value = location.pathname;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var bad = null;
      form.querySelectorAll("[required]").forEach(function (f) {
        var ok = f.value.trim() !== "";
        if (f.name === "phone") ok = f.value.replace(/\D/g, "").length >= 10;
        f.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok && !bad) bad = f;
      });
      if (bad) {
        status.className = "form-status err";
        status.textContent = bad.name === "phone" ? "Please enter a 10 digit phone number." : "Please fill in your name, phone and what you need help with.";
        bad.focus();
        return;
      }
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      btn.textContent = "Sending...";
      var data = {};
      new FormData(form).forEach(function (v, k) { if (k !== "form-name") data[k] = v; });
      data._subject = "New estimate request from jqplumbingllc.com";
      data._template = "table";
      data._replyto = data.email || "";
      fetch(C.FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      }).then(function (j) {
        if (j && (j.success === false || j.success === "false")) throw new Error(j.message || "failed");
        form.classList.add("sent");
        status.className = "form-status ok";
        status.textContent = "Thanks! Your request was sent. We will get back to you soon. Need us sooner? Call 210-793-6046.";
        track("generate_lead", {
          form_name: "estimate",
          service: form.service ? form.service.value : "",
          page_path: location.pathname
        });
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = "Request my free estimate";
        status.className = "form-status err";
        status.textContent = "That did not go through. Please try again or call 210-793-6046.";
      });
    });
  });

  /* Services dropdown (desktop): click or keyboard toggles it, hover is handled in CSS */
  var menuItem = document.querySelector(".has-menu");
  var menuBtn = menuItem && menuItem.querySelector(".menu-btn");
  function setMenu(open) {
    if (!menuItem) return;
    menuItem.classList.toggle("open", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  if (menuBtn) {
    menuBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      setMenu(!menuItem.classList.contains("open"));
    });
    document.addEventListener("click", function (e) { if (!menuItem.contains(e.target)) setMenu(false); });
    menuItem.addEventListener("focusout", function (e) { if (!menuItem.contains(e.relatedTarget)) setMenu(false); });
  }

  /* Mobile menu */
  var burger = document.querySelector(".burger");
  var mMenu = document.getElementById("m-menu");
  function setMobile(open) {
    mMenu.hidden = !open;
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("menu-open", open);
  }
  if (burger && mMenu) {
    burger.addEventListener("click", function () { setMobile(mMenu.hidden); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    setMenu(false);
    if (burger && mMenu && !mMenu.hidden) { setMobile(false); burger.focus(); }
  });

  /* Contact page: preselect the service when arriving from a service page (?service=slug) */
  var svcParam = new URLSearchParams(location.search).get("service");
  if (svcParam) {
    var map = {
      "drain-cleaning-san-antonio": "Drain cleaning or clog",
      "sewer-camera-inspection-san-antonio": "Sewer camera inspection",
      "water-heater-repair-san-antonio": "Water heater",
      "water-treatment-san-antonio": "Water treatment system",
      "leak-detection-san-antonio": "Water leak",
      "emergency-plumber-san-antonio": "Burst pipe or urgent repair",
      "fixture-replacement-san-antonio": "Fixture or faucet replacement",
      "plumbing-repair-san-antonio": "Plumbing repair",
      "tunnel-work-san-antonio": "Under slab or tunnel work",
      "commercial-plumbing-san-antonio": "Commercial plumbing"
    };
    var sel = document.querySelector('form.form select[name="service"]');
    if (sel && map[svcParam]) sel.value = map[svcParam];
  }

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
