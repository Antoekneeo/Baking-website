# CookieBook – Wireframe Implementation

This project is a minimal Flask app with a responsive landing page that matches the provided wireframe. The page includes a sticky header with logo and navigation, a hero section with headline and call‑to‑action, an evenly spaced recipe card grid, and a centered footer. Mobile uses a hamburger menu.

## What I changed
- Replaced `templates/index.html` with a responsive layout using semantic HTML, scoped CSS, and a tiny JS menu toggle.
- Left `app.py` untouched other than using it to serve the updated template.
- Added this README.

## Files
- `app.py` – Flask entrypoint with `/` route rendering `index.html`.
- `templates/index.html` – All HTML, minimal CSS, and a small JS snippet for mobile navigation.
- `README.md` – Documentation and run instructions.

## How the wireframe is represented
- **Header**: Sticky, logo on the left, horizontal nav on desktop. On mobile: centered brand and hamburger menu that expands links.
- **Hero**: Left placeholder media box (dashed border) and right headline “Bake Something Sweet” with primary CTA “Explore Recipes”. Stacks vertically on smaller screens.
- **Grid**: Four recipe cards per row on desktop, two on tablets, one on mobile. Cards have image placeholder, category, title, and a prominent "View Recipe" button.
- **Footer**: Single centered line of text.

## Design details
- Typography: Google Fonts Inter (weights 400/600/700).
- Color/system tokens: defined as CSS custom properties for easy tweaks.
- Layout container: `max-width: 1100px;` with side padding.
- Accessibility: Semantic tags (`header`, `nav`, `main`, `section`, `article`, `footer`). ARIA attributes on the hamburger button and list section label.
- Touch targets: Buttons are 40–44px tall for mobile usability.

## Run locally
1. Ensure Python and Flask are installed.
   ```bash
   pip install flask
   ```
2. From the project root, run:
   ```bash
   python app.py
   ```
3. Open http://127.0.0.1:5000 in your browser.

## Customization tips
- Update navigation labels/links inside the `nav.links` block.
- Replace placeholder media boxes by placing images where `.hero-media` and `.card-media` elements are.
- Adjust breakpoints or grid columns in the `@media` rules in the `<style>` block.

## Future enhancements (optional)
- Extract CSS/JS into static files.
- Hook recipe cards to real data and routes.
- Add dark mode using an additional `data-theme` set of CSS variables.
