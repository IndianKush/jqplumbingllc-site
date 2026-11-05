/* ============================================================
   TRACKING SETUP. Paste your IDs here. This is the only edit needed.
   GA4_ID:       Google Analytics 4 measurement ID, like "G-ABC123XYZ"
   ADS_ID:       Google Ads conversion ID, like "AW-123456789"
   ADS_CALL_LABEL / ADS_LEAD_LABEL: conversion labels from Google Ads
   Leave a value as "" to switch that part off.
   ============================================================ */
window.JQ_CONFIG = {
  GA4_ID: "",
  ADS_ID: "",
  ADS_CALL_LABEL: "",
  ADS_LEAD_LABEL: "",
  /* Where estimate requests are emailed (FormSubmit). After Jon activates it,
     swap the email for the random alias FormSubmit sends him, to hide the address from spammers. */
  FORM_ENDPOINT: "https://formsubmit.co/ajax/Jonq@jqplumbingllc.com"
};

(function () {
  var C = window.JQ_CONFIG;
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  var firstId = C.GA4_ID || C.ADS_ID;
  if (firstId) {
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(firstId);
    document.head.appendChild(s);
    gtag("js", new Date());
    if (C.GA4_ID) gtag("config", C.GA4_ID);
    if (C.ADS_ID) gtag("config", C.ADS_ID);
  }

  /* Fires one event two ways:
     1. dataLayer.push({event: name}) for Google Tag Manager triggers
     2. gtag event for GA4, plus a Google Ads conversion when a label is set */
  function track(name, params, adsLabel) {
    params = params || {};
    var payload = { event: name };
    for (var k in params) payload[k] = params[k];
    dataLayer.push(payload);
    if (firstId) {
      gtag("event", name, params);
      if (C.ADS_ID && adsLabel) gtag("event", "conversion", { send_to: C.ADS_ID + "/" + adsLabel });
    }
  }
  window.jqTrack = track;

  /* Click to call: every tel: link on the site */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"]');
    if (!a) return;
    track("call_click", {
      link_location: a.getAttribute("data-call-location") || "other",
      page_path: location.pathname
    }, C.ADS_CALL_LABEL);
  });

  /* Estimate form: validates, posts to Netlify Forms, fires generate_lead only on success */
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
        }, C.ADS_LEAD_LABEL);
      }).catch(function () {
        btn.disabled = false;
        btn.textContent = "Request my free estimate";
        status.className = "form-status err";
        status.textContent = "That did not go through. Please try again or call 210-793-6046.";
      });
    });
  });

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
