# Sparks OT Migration

Migrating sparksot.com from Squarespace to a static site for Cloudflare Pages.
This is a demo build to show the client the migration is feasible and will save
her money.

## Stack

Multi-file static site: HTML + CSS + minimal JS. No framework. No build step.
Each page is a standalone .html file that loads a shared stylesheet and minimal
JS. This needs to be deployable to Cloudflare Pages with zero configuration.

## Folder structure

- `/site/` — the finished website. This is what gets deployed.
- `/assets-raw/` — original Drive download. Treat as read-only reference material.
- `/scripts/` — helper scripts for extracting copy, processing assets, etc.

## Design direction

- **Type:** Cormorant Garamond from Google Fonts, substituting the original's
  Orpheus Pro. Pair with a clean sans-serif (your choice — something that
  complements without competing).
- **Palette:** sage green dominant, warm cream background, sand/tan CTA buttons,
  dusty pink used sparingly as an accent.
- **Tone:** earthy, warm, professional. Aimed at parents researching pediatric
  OT for their kids — not at the kids themselves.
- **Approach:** modernize the Squarespace original. Keep it recognizably hers
  (same logo, same general feel) but improve typography rhythm, spacing,
  hierarchy, and motion. Don't make it generic.

## Pages and sections

### Home

- Hero with the kid-in-nature photo, headline, subhead, primary CTA
- Intro about Korrie and her practice
- Photo gallery of the clinic (grid or scrollable)
- "Does your child ever..." symptom list — consolidate the original's overlong
  version into a cleaner two-column layout
- Therapeutic approach section
- Rotating testimonial carousel
- CTA strip with the physical address

### Team

Bios for:
- Korrie Sparks (OTD, OTR/L)
- Julia Colton (MSOT, OTR/L)
- Anna Kopatich (OTR/L)
- Devin Hardy (Clinic Operations Manager)
- Darcy the therapy dog

Paraphrase bio copy from the original — don't reproduce it verbatim.

### Contact

- Contact form: first name, last name, email, message
- Email address (pull from original site)
- Physical address: 3015 47th Street Suite E4, Boulder CO 80301
- Wire the form to Formspree or Cloudflare Pages Functions — decide during
  build based on which is simpler for the demo

## Technical requirements

- Mobile-first responsive
- Scroll-reveal animations that respect `prefers-reduced-motion`
- Sticky header with hamburger nav on mobile
- Semantic HTML throughout
- Proper form labels, visible focus styles, accessible color contrast
- Use `python3 -m http.server` from inside `/site/` for local testing — opening
  HTML files directly causes font CORS issues

## Working rules

- **Be ruthless about context.** Don't paste large file contents into the
  conversation. Write to files and reference them by path.
- **Don't re-list directories you've already seen.** Build a manifest once,
  then refer to it.
- **Skip the Squarespace CSS/JS bundles entirely.** They're useless for our
  purposes. The HTML files are only useful for extracting copy.
- **Flag any AdobeStock-licensed assets** before using them so the license
  can be confirmed for self-hosting.
- **Use scripts for bulk extraction.** When pulling copy from the three HTML
  files, write a Python script rather than reading them inline.
