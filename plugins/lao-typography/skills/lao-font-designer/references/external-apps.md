# Lao fonts in external design applications

Read only the section for the target application and the common checks. These workflows cover font integration and testing; building a font also requires glyph mapping, metrics, shaping, compilation, and validation in a font-authoring toolchain.

Provider documentation checked on 2026-10-26. Recheck current documentation when the user's version, plan, permissions, or available controls differ. Supported file formats do not guarantee correct Lao shaping.

## Adobe Illustrator, InDesign, and Photoshop

Identify the specific Adobe application and version. Make the exact licensed font and required weights available to that app, then test actual Lao text. Do not assume an Adobe Fonts activation grants permission to copy its font files into another service. Adobe documents restrictions on packaging and copying font files; use the applicable license and delivery method. [Adobe font packaging guidance](https://helpx.adobe.com/ph_fil/fonts/web/getting-and-using-fonts/package-font-files.html)

- **InDesign:** use the World-Ready Composer for Lao paragraphs, then define paragraph and character styles with the intended font, size, leading, and tracking. Adobe explicitly lists Lao among its supported scripts. Check stacked marks, line breaks, overset text, and the exported PDF. [World-Ready Composer](https://helpx.adobe.com/in_hi/indesign/desktop/language-and-proofing/language-settings/adobe-world-ready-composer-overview.html)
- **Photoshop:** keep Lao in editable type layers while designing. Current Photoshop uses its Unified Text Engine; do not prescribe obsolete engine-switching instructions by default. Adobe lists Lao support but notes that typography and editability can differ across applications. Check both the text layer and final raster output. [Unified Text Engine](https://helpx.adobe.com/photoshop/desktop/text-typography/international-text-languages/overview-of-unified-text-engine.html), [supported scripts](https://helpx.adobe.com/uk/photoshop/desktop/text-typography/international-text-languages/supported-international-scripts.html)
- **Illustrator:** inspect the installed version's text/composer controls and test Lao shaping rather than assuming InDesign settings exist there. Use live text for specimens and wordmarks. Vector glyph artwork can be prepared here, but it must enter a font-authoring workflow to become mapped, shaped font characters. Retain an editable master before creating any outlined delivery copy.

Avoid using manual mark repositioning as a substitute for repairing a reusable font. A visual adjustment to a logo does not fix typing, search, or shaping elsewhere.

## Figma

Figma documents TTF/OTF support. For local fonts, distinguish the desktop app from the browser: the desktop includes its font helper, while browser access requires the font installer. Collaborators need access to the same styles. Figma also documents account font uploads for MCP/agent access; do not assume a locally visible font is available to automation. Check the actual connection and font availability before editing. [Add a font to Figma](https://help.figma.com/hc/en-us/articles/360039956894-Add-a-font-to-Figma)

Create editable Lao text layers and reusable text styles for the needed heading, body, and caption roles. Record family, weight, size, line height, and letter-spacing. Test auto-layout, resizing, long labels, and combining marks. Avoid detaching text or outlining it merely to conceal missing-font problems.

Compare the file with a requested PDF, SVG, or raster export. Report whether the chosen export retains text or converts it, and whether the result meets the user's editing and accessibility needs. A screenshot alone does not establish correct text extraction or collaborator access.

## Canva

Check the account's current Brand Kit upload eligibility and role before planning custom-font integration. Canva documents OTF, TTF, and WOFF uploads and requires appropriate embedding rights. Its current guidance says variable fonts are unsupported; use permitted static files for the required weights. [Upload and use Brand Kit fonts](https://www.canva.com/en_au/help/upload-fonts/)

Use a suitable existing library font or upload the licensed custom font within the requested scope. Set the applicable Brand Kit text roles and test actual Lao in editable text boxes. Check letter-spacing, line spacing, stacked marks, and wrapping at the final design size. Do not silently change shared brand defaults when only one design was requested.

Inspect downloaded output as well as the editor. Canva notes that a successful upload can still produce font errors in a design or download. If compatibility fails, record the affected font and text and test another authorized font or build. [Font upload troubleshooting](https://www.canva.com/en_au/help/font-upload-error/)

## Common specimen and delivery checks

Use the same approved source strings across applications, including upper vowels with tone marks, lower vowels, tall consonants, prefixed vowels, special consonant forms, digits, currency, and mixed Lao/English text. Label constructed glyph stress tests as tests, not vocabulary.

Start with zero tracking, actual font weights, and enough leading for stacked marks; inspect results rather than assuming identical numerical settings render identically across apps. Preserve base/mark clusters, correct Unicode, and supplied wording. Keep generated artwork separate from font-set Lao text.

Record app/version, font/version, style settings, tested strings, observed defects, and export format. Check clipping, fallback, mark collisions, line breaks, and editability. Test text extraction when the requested output should retain text. Mark checks as passed, failed, or not tested; a successful install or upload is not a rendering pass.
