# Google Reviews integration — Enigma Dent

The site is ready for optional Google Places API (New) reviews.

Add to `.env`:

```env
GOOGLE_PLACE_ID=your_google_place_id
GOOGLE_PLACES_API_KEY=your_google_places_api_key
```

The homepage then requests rating, review count and up to five reviews, caches them for 6 hours, and shows author attribution.

Without these variables, the site remains fully functional and shows a button to open Enigma Dent in Google Maps.

If you want a no-Maps-billing integration with all reviews from a Business Profile that you own/manage, use Google Business Profile APIs instead. That requires Google OAuth/business-profile access and is a separate integration step.
