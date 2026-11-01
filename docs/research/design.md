# Design research: Greek teacher guide (micro:bit + Nezha)

Method note: web search and fetch were partly limited (no PDF layouts could be opened; one fetch timed out). Claims below carry a URL where a source was found. Items tagged **[unverified]** are my design judgement or prior knowledge, not confirmed in this session. Check them before relying on them.

## 1. Exemplary educational design systems

- **micro:bit Educational Foundation.** Lessons are mostly web-based, with lesson plans, videos, guided tutorials, quizzes, challenges and answers, each sized for a single lesson block. https://makecode.microbit.org/lessons/teach . Hub: https://microbit.org/teach. Borrow: the repeatable "guide + student-facing page" split and challenge cards. Visual specifics not verified.
- **Raspberry Pi Foundation / Teach Computing Curriculum.** Each unit has an overview, a learning graph, and per-lesson plans, slides and worksheets. Lessons are numbered in teaching order, and formative-assessment moments and misconceptions are listed in the plan. https://teachcomputing.org/curriculum , https://blog.teachcomputing.org/how-to-use-learning-objectives-graphs-to-plan-progression/ . Borrow: the "misconceptions" slot, which maps to your "what will go wrong" table. Also borrow the unit-level overview page.
- **Code.org CS Fundamentals.** One common lesson template with overview first, then a core activity with timing, plus implementation tips, differentiation and extensions. https://code.org/curriculum/docs/csf/CSF_Curriculum_Guide_2018_smaller.pdf , https://code.org/curriculum/docs/k-5/complete.pdf . Borrow: overview-first lesson page, so the teacher can decide in 10 seconds whether to read on.
- **LEGO Education SPIKE.** Themed units. Each lesson has preparation, a teacher-support section, step-by-step facilitation based on the 5E model, tips, differentiation and extensions. Lessons rise in difficulty toward a final project. https://education.lego.com/en-us/teacher-resources/lego-education-spike-essential/lesson-planning/lego-education-spike-essential-lesson-planning-intro . Borrow: prep / run / tips / extend order, plus vocabulary pre-teaching.
- **Creative Computing Curriculum Guide (ScratchEd, Harvard).** About 154 pages, openly licensed (CC BY-SA for the draft), design-based sessions. https://scratched.gse.harvard.edu/guide , https://scratched.gse.harvard.edu/resources/scratch-curriculum-guide-draft.html . Borrow: reflection prompts and student-facing "debug it" cards. Layout not inspected.
- **Barefoot Computing.** Packs of lesson plan, slides, worksheet; cross-curricular and unplugged. https://barefootcomputing.org/about-barefoot , https://microbit.org/news/2022-03-23/new-recycling-and-wildlife-primary-lessons-from-barefoot . Borrow: a pack structure of plan + student sheet.
- **Hello Ruby.** Story-driven, for ages 4 to 10, with a companion site of mostly screen-free activities. https://helloruby.com . Borrow: character and illustration warmth. A mascot or recurring "inventor" figure is **[unverified]** as a fit.
- **DK Eyewitness.** Design traits I could source: imagery set against white backgrounds, strong labelling and captioning, and deliberate use of space. https://medium.com/charting-ahead/iconic-visionaries-of-design-dorling-kindersley-d3fcb236adff , https://worddisk.com/wiki/Eyewitness_Books . General modular-grid advice: consistent modules, not every module filled, white space on the outside rather than trapped between elements. https://yearbookology.friesens.com/docs/chapter-2-layout-styles , https://www.walsworthyearbooks.com/?p=2059 . No official DK style guide was found.
- **Not researched:** Khan Academy and Twinkl style sheets, as no sources were found.

Synthesis (mostly **[unverified]** judgement): all the sources above use a fixed lesson template with the same order every time. Teachers learn the template once. Your 16-lesson template already matches this practice.

## 2. Greek typography

Verification status: only Commissioner's Greek support was confirmed, and weakly. The others rest on my knowledge. Check each at https://fonts.google.com/?subset=greek before committing. Also confirm that the italic and bold files you need exist for Greek.

- **Commissioner** (Kostas Bartsokas). Variable font with Latin, Greek and Cyrillic, SIL OFL, with Thin to Black and italics. One review says the italic is a slanted roman rather than a true italic. https://github.com/kosbarts/Commissioner , https://pimpmytype.com/font/commissioner/ . An openSUSE card puts Greek coverage at 14.3% of its tracked glyph set, so test the full alphabet with accents and diaeresis (ΐ, ΰ, ά). https://fontinfo.opensuse.org/fonts/CommissionerBold.html . Best use: headings, level chips, big numerals.
- **Noto Sans.** Safe fallback with full Greek (including polytonic) and real italics **[unverified]**. Wide and slightly neutral. Good body or fallback.
- **Source Sans 3.** Narrow, readable, with real Greek italics **[unverified]**. A good body face at 10 to 10.5 pt for dense tables.
- **Fira Sans.** Friendly, humanist, many weights, Greek included **[unverified]**. Good for headings or UI-like labels such as port names.
- **IBM Plex Sans.** Greek included, slightly technical feel **[unverified]**. Pair its Mono sibling for code snippets.
- **Manrope.** Geometric, modern. Greek support **[unverified]**: I did not confirm it. Do not choose without checking.
- **Serif body options.** Literata and Source Serif 4 have Greek **[unverified]**. A serif body feels "bookish" but is weaker in small table cells.

Recommended pairing (verify first): **Commissioner** (headings, 600 to 800) with **Source Sans 3** (body 10.5 pt), or all-**Noto Sans** as the lowest-risk option. Code font: IBM Plex Mono or Noto Sans Mono, if Greek comments are not needed.

Sizes for A4 teacher material **[unverified, standard practice]**:

| Element | Size | Line-height |
|---|---|---|
| Body | 10.5 to 11 pt | 1.4 to 1.5 |
| Table cell | 9.5 to 10 pt | 1.3 |
| H1 / H2 / H3 | 26 / 17 / 12.5 pt | 1.15 to 1.25 |
| Caption | 8.5 to 9 pt | 1.3 |

- Line length is 60 to 75 characters. Use one wide column, with an optional narrow margin sidebar.
- Greek accents need extra leading. Set ALL CAPS headings without accents carefully: Greek convention drops tonos in capitals.
- Embed fonts in the PDF so printing at school does not substitute them.

## 3. Colour systems

Standards (confirmed): body text needs 4.5:1 contrast, large text 3:1, and meaningful graphics or UI borders 3:1. Large means 18 pt or more, or 14 pt bold or more. https://w3c.github.io/wcag/understanding/contrast-minimum.html , https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast . Unchanged in WCAG 2.2. https://webaim.org/articles/contrast/

Rule for print: also encode level by dots and the word label, never by colour alone. School printers are often greyscale.

Suggested palette (hex values are my proposals **[unverified]**; run each through a contrast checker such as https://webaim.org/resources/contrastchecker/):

| Use | Hex | Text on it |
|---|---|---|
| Ink (body text) | #1F2937 | on white, high contrast |
| Level 1 (teal) | #0F766E | white text |
| Level 2 (green) | #3F7D20 | white text |
| Level 3 (amber) | #B45309 | white text |
| Level 4 (orange-red) | #C2410C | white text |
| Level 5 (purple) | #6D28D9 | white text |
| Tip (blue tint) | bg #E8F1FB, bar #1D4ED8 | ink |
| Warning (yellow tint) | bg #FFF4D6, bar #B45309 | ink |
| Safety (red tint) | bg #FDE8E8, bar #B91C1C | ink |
| Teacher note (grey tint) | bg #F1F5F9, bar #475569 | ink |

- Pale tints are backgrounds only. Put dark ink text on them.
- Level 1 to 5 colours are for chips, header bands and dots. Do not use them for long text.
- Difficulty signalling: dots (●●○○○), stars, or colour chips. Your dots plus a one-word label plus the colour is a three-way redundant signal, which is good.
- Publisher practice for difficulty could not be sourced beyond the LEGO "lessons progress in difficulty" note above.

## 4. Component patterns

None of the specifics below were sourced from a PDF I opened. Treat as **[unverified]** design recommendations consistent with the Code.org and LEGO lesson templates above.

- **Lesson header card ("at a glance"):** level chip, dots, duration, group size, one-line goal, lesson id (e.g. M3-07). Full width, tinted band in the level colour.
- **Callouts:** left colour bar (4 pt), small icon, bold label (Tip / Warning / Safety / Teacher note), tinted background. Use a bordered div, not a table. Avoid more than two per page.
- **Steps:** large numbered circles, one action per step, a screenshot or photo right of the text.
- **Materials list:** a grid of small icon tiles with quantity and port label. Prefer this to a table.
- **Layout:** A4 portrait, one main column with 20 to 22 mm margins and a 55 mm side margin for captions, vocabulary and "why" notes. This follows the DK idea of modules plus captions, https://yearbookology.friesens.com/docs/chapter-2-layout-styles . Reserve two columns for short lists only.
- **Code screenshot placement:** put the screenshot immediately after the goal and before the block-by-block table, at full or two-thirds width, with numbered markers matching the table rows. Explanation goes below or beside it, never on another page.
- **Troubleshooting:** a 3-column "symptom / likely cause / fix" table is a legitimate table use. Keep it compact.
- **QR codes:** one per lesson, bottom corner of the last page, for the .hex or MakeCode project link. Put the short URL in text next to it for print.
- **Footer:** lesson id, title, page number, guide version.
- **Challenge card:** a dashed-border box, can be cut out. Keep it on its own half-page so it can be handed out.

## 5. Delivery format comparison

- **(a) Google Doc.** Pros: comments, easy sharing. Cons: no callout style. Workarounds are a single-cell table, the Drawing tool, or paragraph borders and shading, and text boxes are fragile. https://thebricks.com/resources/how-to-box-text-in-google-docs-a-step-by-step-guide . Custom Word styles can be flattened on conversion. https://cloud.motorsport.unibo.it/article/the-effortless-way-to-convert-word-docs-to-google-docs-in-2024 (low-quality source, treat as a lead). Verdict: this is the root of the "ugly" result. Keep it only as a viewing/commenting copy.
- **(b) HTML + print CSS to PDF.** Paged.js is a JS polyfill for CSS Paged Media that runs in a browser (typically with headless Chrome). WeasyPrint is a standalone Python engine with strong paged-media support, but no JavaScript. https://www.github.com/singlesourcepub/community/discussions/49 , https://www.pistack.xyz/posts/2026-06-25-self-hosted-pdf-document-generation-weasyprint-wkhtmltopdf-typst-pagedjs/ (secondary sources, no rigorous benchmark exists). Official sites: https://www.pagedjs.org/ , https://www.weasyprint.org/ (the WeasyPrint fetch timed out, so I did not read it). Pros: full control of fonts, grid, callouts and page footers, and one source gives both web and PDF. It also suits regeneration from markdown: markdown, then HTML template, then PDF. Cons: teachers cannot edit it easily.
- **(c) .docx with a real style set.** Teachers can edit it, and the structure survives in Word and LibreOffice. Google Drive can edit a .docx in place without converting it, so the format and styles are kept. https://blogs.swarthmore.edu/its/2026/07/31/no-google-drive-i-wanted-a-word-document/ . Cons: callout boxes need paragraph borders and shading, and fine layout control is weaker than HTML.
- **(d) Canva / Google Slides.** Visual, but painful at 30 to 50 pages and not regenerable from markdown. Use it only for the poster and role cards **[unverified judgement]**.

**Recommendation:** primary is HTML + print CSS to PDF (WeasyPrint for a simple, scriptable pipeline, Paged.js if you want in-browser preview). Secondary is a styled .docx generated from the same markdown (for example via pandoc with a reference .docx, **[unverified]** tooling choice) so teachers can edit and comment. Publish the PDF as the canonical print version and the .docx as the editable copy. Keep the Google Doc only if people need comment threads.

## 6. Greek educational design references

- **ΙΕΠ Εργαστήρια Δεξιοτήτων PDFs** (teacher training programmes, 2023): e.g. "Ρομποτική με Arduino", "Σχεδιάζουμε ένα ρομπότ". https://ftp.iep.edu.gr/images/IEP/skill-labs/2023/ΠΡΟΓΡΑΜΜΑΤΑ_ΕΠΙΜΟΡΦΩΣΗΣ_/ΡΟΜΠΟΤΙΚΗ_ΜΕ_ARDUINO.pdf , https://web.archive.org/web/20261004214942/https://www2.iep.edu.gr/images/IEP/skill-labs/2023/%CE%A0%CE%A1%CE%9F%CE%93%CE%A1%CE%91%CE%9C%CE%9C%CE%91%CE%A4%CE%91_%CE%95%CE%A0%CE%99%CE%9C%CE%9F%CE%A1%CE%A6%CE%A9%CE%A3%CE%97%CE%A3_/%CE%A3%CE%A7%CE%95%CE%94%CE%99%CE%91%CE%96%CE%9F%CE%A5%CE%9C%CE%95_%CE%95%CE%9D%CE%91_%CE%A1%CE%9F%CE%9C%CE%A0%CE%9F%CE%A4.pdf . The search snippets show text-heavy training documents with funding boilerplate (ΕΠ «Ανάπτυξη Ανθρώπινου Δυναμικού 2014-2020»). I did not open them to judge layout, so any statement that they look dated is **[unverified]**.
- **ebooks.edu.gr** offers school books as PDF, open HTML, enriched interactive HTML/PDF, a PDF with fonts for students with low vision, and i-book. https://lb2.ebooks.edu.gr/info/ebooks.edu.gr_MANUAL_2024-10-29-v1.3.pdf . Takeaway: an official precedent exists for a low-vision PDF variant. Consider offering a large-print version of the guide.
- **Other Greek STEM material:** an ΕΛ/ΛΑΚ Arduino robotics PDF exists. https://edu.ellak.gr/wp-content/uploads/sites/11/2021/05/%CE%93%CE%B5%CF%89%CF%81%CE%B3%CE%B9%CF%84%CE%B6%CE%AF%CE%BA%CE%B7-%CE%9D%CE%B1%CF%84%CE%B1%CE%BB%CE%AF%CE%B1-%CE%98%CE%B5%CF%8C%CE%BA%CE%BB%CE%B5%CE%B9%CE%B1-%CE%A0%CE%9586-%CE%95%CE%BA%CF%80%CE%B1%CE%B9%CE%B4%CE%B5%CF%85%CF%84%CE%B9%CE%BA%CE%AE-%CF%81%CE%BF%CE%BC%CF%80%CE%BF%CF%84%CE%B9%CE%BA%CE%AE-%CE%BC%CE%B5-arduino_comp.pdf
- What to avoid **[unverified, from general Greek-publishing experience]**: Times New Roman-style default fonts, all-caps headings with accent errors, long unbroken text, and mixed Greek/Latin technical terms without a glossary. Decide once whether block names stay in English (as in MakeCode) and show the Greek gloss beside them.

## Recommendation summary

1. Use one fixed lesson template with the same section order on every lesson, as Code.org and LEGO do.
2. Put an "at a glance" header card first: level chip, dots, time, group size, goal, lesson id.
3. Build on a modular grid with generous outer white space, captions and labels, in the DK manner.
4. Fonts: Commissioner for headings, Source Sans 3 (or Noto Sans) for body; verify Greek glyphs and italics on fonts.google.com first.
5. Body 10.5 to 11 pt, line-height 1.4 to 1.5; embed fonts in the PDF.
6. Five level colours plus four semantic callout colours, all at WCAG 4.5:1 for text; always add dots and a word label for greyscale printing.
7. Callouts as bordered divs with a colour bar, icon and label; tables only for real tabular data.
8. Place the code screenshot with numbered markers directly above the block-by-block table.
9. Primary format: HTML + print CSS to PDF (WeasyPrint or Paged.js) generated from markdown; secondary: a styled .docx from the same source for teacher edits.
10. Offer a large-print or low-vision variant, and keep Canva only for the poster and role cards.
