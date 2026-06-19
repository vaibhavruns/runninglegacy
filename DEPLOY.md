# Deploying STRIDE to vpontherun.com (Render + Cloudflare)

This moves the site off Streamlit Community Cloud onto Render, with your own
domain `vpontherun.com` and free SSL. Same `app.py`, same GitHub workflow.

-----

## 0. Repo prerequisites (one-time)

Make sure these are committed to the **root** of the `runninglegacy` repo:

- `app.py`
- `requirements.txt`   (new — included alongside this file)
- All 8 data CSVs the app reads (activities.csv, athlete_profile.csv,
  daily_metrics.csv, fit_metrics.csv, garmin_activities.csv, locations.csv,
  nrc_monthly.csv, zones.csv)

> Push these from your phone or a non-office network (office blocks GitHub).
> Drag the files into GitHub’s “Upload files” — never paste.

-----

## 1. Create the Render web service

1. Go to <https://render.com> and sign up / log in **with GitHub**.
1. **New → Web Service** → connect the `runninglegacy` repo.
1. Fill in:
- **Language / Environment:** Python 3
- **Build command:**
  
  ```
  pip install -r requirements.txt
  ```
- **Start command:**
  
  ```
  streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
  ```
- **Instance type:** Free to start (it sleeps when idle; upgrade to
  Starter ~$7/mo later to keep it always-on).
1. (Recommended) Add an environment variable so the Python version matches
   what the app was built against:
- Key: `PYTHON_VERSION`  Value: `3.12.4`
1. **Create Web Service.** Render builds and gives you a URL like
   `https://stride-xxxx.onrender.com`. Confirm the site loads there first.

> After this, every push to the repo auto-deploys. No more manual reboot.

-----

## 2. Add your domain in Render

1. Open the service → **Settings → Custom Domains → Add Custom Domain**.
1. Add **both**:
- `vpontherun.com`
- `www.vpontherun.com`
1. Render shows a target hostname (your `*.onrender.com`) and verification
   status for each. Keep this tab open — you’ll paste the target into Cloudflare.

-----

## 3. Point Cloudflare DNS at Render

In the Cloudflare dashboard → select `vpontherun.com` → **DNS → Records**.

Add two CNAME records (Cloudflare flattens CNAME at the root automatically):

|Type |Name |Target (use the value Render showed you)|Proxy status             |
|-----|-----|----------------------------------------|-------------------------|
|CNAME|`@`  |`stride-xxxx.onrender.com`              |**DNS only (grey cloud)**|
|CNAME|`www`|`stride-xxxx.onrender.com`              |**DNS only (grey cloud)**|


> IMPORTANT: set proxy to **DNS only (grey cloud)**, not proxied (orange),
> at least until SSL is issued. With the orange cloud on, Render can’t
> validate the domain or issue its Let’s Encrypt certificate. You can revisit
> Cloudflare proxying later, but grey cloud is the clean, working default.

If Render gives you an **A record / IP** for the root instead of a CNAME,
add that as an `A` record on `@` with the IP they provide (same grey-cloud rule).

-----

## 4. Wait + verify

- Back in Render’s Custom Domains panel, the status moves to **Verified**, then
  Render issues SSL automatically (usually minutes, up to ~1 hour).
- Visit **<https://vpontherun.com>** — you should see the site with a padlock.

-----

## 5. Pick one canonical address (optional but tidy)

Decide whether `vpontherun.com` or `www.vpontherun.com` is primary. In Render’s
Custom Domains, you can set one to **redirect** to the other so links are
consistent. Recommended: redirect `www` → `vpontherun.com`.

-----

## 6. Retire the old Streamlit Cloud app (optional)

Once `vpontherun.com` is live, the old `runninglegacy-vaibhav.streamlit.app`
can be left as-is or deleted from Streamlit Community Cloud. Render is now
canonical.

-----

## Ongoing workflow

- Edit `app.py` → push to GitHub (from phone / home network) → Render
  auto-deploys in ~1–2 min. No manual reboot needed.
- Data update: replace a CSV in the repo root, push, auto-deploys.

## Troubleshooting

- **App builds but page won’t connect / keeps loading:** add these flags to the
  start command and redeploy —
  `--server.enableCORS false --server.enableXsrfProtection false`
- **SSL stuck “pending”:** confirm the Cloudflare records are **grey cloud**
  (DNS only), not orange (proxied).
- **Free instance slow on first hit:** that’s the idle-sleep wake (~30–50s).
  Upgrade to the Starter instance to remove it.