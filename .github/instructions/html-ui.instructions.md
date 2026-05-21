---
applyTo: "src/**/*.html"
description: "Guide Copilot when generating HTML: use Bootstrap UI patterns and avoid inline styles by using the shared stylesheet"
---

# HTML Generation Guidelines

When generating or editing HTML in this repository, follow these rules.

## Styling rules
- Do not use inline style attributes.
- Do not add embedded style blocks in HTML files.
- Put custom styling in `src/_assets/style.css`.
- Link the shared stylesheet in page head as `/_assets/style.css`.

## UI framework
- Use Bootstrap classes for layout and components.
- Include Bootstrap CSS using the official CDN link in the head when missing.
- Use Bootstrap utility classes for spacing, typography, and alignment before adding custom CSS.
- Use semantic HTML with Bootstrap patterns (container, row, col, navbar, card, button, form controls).

## Maintainability
- Keep HTML clean and component-oriented.
- Prefer reusable partials/includes for repeated UI blocks.
- Keep custom CSS minimal and place it only in `src/_assets/style.css`.
