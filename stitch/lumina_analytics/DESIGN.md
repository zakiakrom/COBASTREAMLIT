# Design System Document

## 1. Overview & Creative North Star: "The Digital Atrium"

This design system is a transition from the heavy, high-contrast "neon-on-dark" dashboard era into a sophisticated, editorial light mode experience. Our Creative North Star is **"The Digital Atrium."** Like an atrium, the interface must feel flooded with light, spacious, and architecturally sound. 

We move away from rigid, boxy templates by using **intentional asymmetry** and **tonal depth**. Instead of defining spaces with harsh lines, we use the interplay of light and subtle shifts in surface color to guide the eye. The goal is a professional, data-centric environment that feels breathable, premium, and human-centric.

---

## 2. Colors & Tonal Architecture

Our palette is rooted in a refined foundation of cool greys and high-clarity whites, punctuated by a signature "Electric Primary" blue that commands attention without overwhelming the senses.

### Color Tokens
*   **Background (Canvas):** `#f5f7f9` (Surface) — The base "floor" of the application.
*   **Primary Accent:** `#0050d5` (Primary) — Used for critical data highlights and main CTAs.
*   **Neutral Text:** `#2c2f31` (On Surface) — High-legibility charcoal, softer than pure black.
*   **Subtle Accents:** `#8e3a89` (Tertiary) — Reserved for secondary data categories and subtle brand moments.

### The "No-Line" Rule
To maintain the high-end editorial feel, **1px solid borders for sectioning are strictly prohibited.** We do not "box" our content. Boundaries must be defined solely through background color shifts. For instance, a sidebar should be defined by the transition from `surface` (`#f5f7f9`) to `surface-container-low` (`#eef1f3`).

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. Use the `surface-container` tiers to create depth:
1.  **Level 0 (Base):** `surface` (`#f5f7f9`)
2.  **Level 1 (Sections):** `surface-container-low` (`#eef1f3`)
3.  **Level 2 (Active Cards):** `surface-container-lowest` (`#ffffff`) — This creates a natural "pop" of white against the grey background.

### The "Glass & Gradient" Rule
For floating elements or hero states, use Glassmorphism. Apply `surface-container-lowest` at 70% opacity with a `backdrop-blur` of 20px. For primary CTAs, use a subtle linear gradient from `primary` (`#0050d5`) to `primary-container` (`#7b9cff`) at a 135-degree angle to add "visual soul" and dimension.

---

## 3. Typography: The Editorial Voice

We utilize a dual-font strategy to balance character with utility. **Manrope** provides a modern, geometric headline presence, while **Inter** handles the heavy lifting of data density.

*   **Display (Manrope):** Large, airy, and bold. Used for high-level KPIs and page titles.
    *   *Display-LG:* 3.5rem (Tracking: -0.02em)
*   **Headlines & Titles (Manrope):** Used to establish hierarchy within cards.
    *   *Headline-SM:* 1.5rem / Medium weight.
*   **Body & Labels (Inter):** Optimized for data legibility.
    *   *Body-MD:* 0.875rem (The workhorse for dashboard metrics).
    *   *Label-SM:* 0.6875rem / All-caps with +0.05em tracking for metadata.

---

## 4. Elevation & Depth: Tonal Layering

Traditional drop shadows are a fallback, not a standard. We achieve hierarchy through the **Layering Principle**.

*   **Ambient Shadows:** When a card requires a "floating" state (e.g., a hovered dashboard widget), use a diffused shadow: `box-shadow: 0 12px 32px -4px rgba(44, 47, 49, 0.06)`. Note the use of the `on-surface` color in the shadow to ensure it looks like a natural occlusion of light.
*   **The "Ghost Border" Fallback:** If a layout becomes too low-contrast for accessibility, use a "Ghost Border": `outline-variant` (`#abadaf`) at **15% opacity**. This provides a hint of structure without breaking the airy aesthetic.
*   **Visual Roundedness:** All primary cards must use the `lg` radius (`1rem`). Smaller elements like buttons or chips use `sm` (`0.25rem`) or `full` (`9999px`) to create a playful but professional contrast.

---

## 5. Components: Precision & Clarity

### Buttons
*   **Primary:** Gradient fill (Primary to Primary-Container), white text, `md` (`0.75rem`) corner radius.
*   **Secondary:** `surface-container-highest` background with `primary` text. No border.
*   **Tertiary:** Ghost style. Transparent background, `primary` text, shifts to `surface-container-low` on hover.

### Input Fields & Search
Fields should use `surface-container-lowest` (`#ffffff`) to contrast against the `surface` background. Use a `px` (1px) Ghost Border. Focus state is indicated by a 2px `primary` bottom-border only, maintaining an editorial, "underlined" look.

### Cards & Data Lists
*   **Rule:** Forbid the use of divider lines. 
*   **Execution:** Use vertical white space (`spacing-4` or `1.4rem`) to separate list items. For tabular data, use alternating row tints of `surface-container-low` instead of horizontal rules.
*   **Data Visualization:** Blue accents (`primary`) should be the hero. Use `secondary-fixed` (`#d5e3fc`) for background bars or inactive chart states to keep the visual weight light.

### Additional Signature Component: The "Metric Glass"
A specialized KPI card using a 10% `primary` tinted background, a `backdrop-blur`, and a large `Display-SM` Manrope value. This highlights the most critical data points of the dashboard with a "premium" feel.

---

## 6. Do's and Don'ts

### Do
*   **Do** use white space as a structural element. If a design feels cluttered, increase the spacing from `3` (`1rem`) to `5` (`1.7rem`).
*   **Do** use subtle gradients in data viz to represent growth or intensity.
*   **Do** nest `surface-container-lowest` cards on `surface-container-low` sections.

### Don't
*   **Don't** use 100% opaque grey borders. It makes the UI look like a legacy spreadsheet.
*   **Don't** use pure black (`#000000`) for text. Use `on-surface` (`#2c2f31`) to maintain the "airy" feel.
*   **Don't** use high-saturation "neon" effects. All vibrancy should be grounded in the professional `primary` blue.
*   **Don't** crowd the edges. Ensure a minimum of `spacing-6` (`2rem`) padding for all major container edges.