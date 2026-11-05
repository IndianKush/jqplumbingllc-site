JQ Plumbing LLC website (jqplumbingllc.com)

HOSTING
GitHub Pages, from the dist folder. dist/CNAME holds the domain.
Form: estimate requests are emailed to Jonq@jqplumbingllc.com through FormSubmit (formsubmit.co).
The very first submission sends Jon an activation email; he must click Activate once.

DOMAIN (GoDaddy DNS). Do NOT change nameservers, Jon's Microsoft 365 email depends on them.
A  @   185.199.108.153 / 185.199.109.153 / 185.199.110.153 / 185.199.111.153
CNAME www  <github user>.github.io
Leave MX, autodiscover, TXT, SRV and every other record alone.

TRACKING
Open dist/js/site.js and fill in the values at the top (GA4_ID, ADS_ID, ADS_CALL_LABEL, ADS_LEAD_LABEL).
Events: call_click (every tel: link, with link_location) and generate_lead (only after a successful form send).
Both also go to dataLayer for Google Tag Manager.

EDITING
Copy, phone, license, areas and reviews live in build.py. Edit, then run: python3 build.py
