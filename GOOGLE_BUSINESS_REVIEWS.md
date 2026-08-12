# Google Business Profile reviews — Enigma Dent

## What is already prepared

The website now stores Google reviews locally in Django instead of requesting Google on every page view.

Models:
- `GoogleReview` — one local copy of every Google review.
- `GoogleReviewStats` — current average rating, total review count and synchronization status.

Public pages:
- `/reviews/` — dedicated Google reviews page.
- Home page — latest 6 visible Google reviews + rating summary.

Admin:
- Google reviews can be searched, filtered by stars/date and hidden from the site.
- Google review statistics show the last synchronization status and any error.

## Data saved per review

- Google review ID
- author display name
- author profile photo URL (if Google returns it)
- star rating (1–5)
- comment text
- review create/update dates
- Enigma Dent reply and reply date
- visibility on the website
- last local sync date
- original Google JSON payload for diagnostics

## After Google approves GBP API access

1. Configure OAuth 2.0 for the approved `Enigma Dent Reviews` Cloud project.
2. Obtain an offline refresh token with Business Profile access.
3. Find the Google Business Profile account ID and Enigma Dent location ID.
4. Put these values into `.env`:

```env
GOOGLE_GBP_CLIENT_ID=
GOOGLE_GBP_CLIENT_SECRET=
GOOGLE_GBP_REFRESH_TOKEN=
GOOGLE_GBP_ACCOUNT_ID=
GOOGLE_GBP_LOCATION_ID=
GOOGLE_GBP_MAPS_URL=
```

5. Run manually:

```bash
python manage.py sync_google_reviews
```

6. When it succeeds, schedule that command once daily on the server (cron/systemd/Docker scheduler).

The command paginates through all reviews returned by Google and uses `update_or_create`, so existing reviews are updated instead of duplicated.

## Local testing before API approval

A saved Google API JSON response can be imported without network access:

```bash
python manage.py sync_google_reviews --from-json google_reviews_sample.json
```

This is useful for testing the UI before Google grants API access.
