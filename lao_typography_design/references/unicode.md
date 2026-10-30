# Lao Unicode and encoding (U+0E80–U+0EFF)

Read this when Lao text is broken, garbled, boxed, mixed with Thai, copied between tools, normalized, searched, counted, or cut. Everything marked "verified" was checked with Python's `unicodedata`.

## 1. Block map

| Range | What | Characters |
|---|---|---|
| U+0E81–U+0EAE | Consonants (27 in everyday use, plus rare Pali/Sanskrit letters) | ກ ຂ ຄ ງ … ຮ |
| U+0EB0, U+0EB2, U+0EB3 | Spacing vowel signs | ະ າ ຳ |
| U+0EB1, U+0EB4–U+0EB7, U+0EBB | Upper vowel signs (combining) | ັ ິ ີ ຶ ື ົ |
| U+0EB8, U+0EB9 | Lower vowel signs (combining) | ຸ ູ |
| U+0EBA, U+0EBC, U+0EBD | Pali virama, semivowel lo (ຫຼ), semivowel nyo (ຽ) | ຺ ຼ ຽ |
| U+0EC0–U+0EC4 | Prefixed vowels (stored before the consonant) | ເ ແ ໂ ໄ ໃ |
| U+0EC6 | Repetition mark | ໆ |
| U+0EC8–U+0ECB | Tone marks (mai ek, mai tho, mai ti, mai catawa) | ່ ້ ໊ ໋ |
| U+0ECC–U+0ECE | Cancellation mark, niggahita, yamakkan | ໌ ໍ ໎ |
| U+0ED0–U+0ED9 | Lao digits 0–9 | ໐ ໑ ໒ ໓ ໔ ໕ ໖ ໗ ໘ ໙ |
| U+0EDC, U+0EDD | Ligature letters ໜ (ຫ+ນ) and ໝ (ຫ+ມ) | ໜ ໝ |
| U+0EDE, U+0EDF | Khmu letters | ໞ ໟ |
| U+20AD | Kip sign | ₭ |

Thai is U+0E00–U+0E7F. The Lao block was laid out in parallel, so a Lao letter is often its Thai twin plus 0x80 (ກ U+0E81 and ก U+0E01; ເ U+0EC0 and เ U+0E40). **Do not convert Thai to Lao by shifting codepoints.** The languages are different; the shift produces nonsense.

### The 27 consonants by class, with codepoints (verified)

- **Mid (8):** ກ U+0E81, ຈ U+0E88, ດ U+0E94, ຕ U+0E95, ບ U+0E9A, ປ U+0E9B, ຢ U+0EA2, ອ U+0EAD
- **High (6):** ຂ U+0E82, ສ U+0EAA, ຖ U+0E96, ຜ U+0E9C, ຝ U+0E9D, ຫ U+0EAB
- **Low (13):** ຄ U+0E84, ງ U+0E87, ຊ U+0E8A, ຍ U+0E8D, ທ U+0E97, ນ U+0E99, ພ U+0E9E, ຟ U+0E9F, ມ U+0EA1, ຣ U+0EA3, ລ U+0EA5, ວ U+0EA7, ຮ U+0EAE

Look-alikes worth proofreading: ບ / ປ, ດ / ຕ, ຜ / ຝ / ພ / ຟ, ຍ / ຢ, ມ / ນ.

## 2. Storage order inside a syllable

Text is stored in this logical order, which is not always the order you see:

`[prefixed vowel] consonant [ຼ] [upper or lower vowel] [tone mark] [ະ າ ຳ] [final consonant]`

- ເກົ້າ is stored ເ, ກ, ົ, ້, າ. The ເ comes first in memory and on screen but is read after ກ.
- ນ້ຳ is stored ນ (U+0E99), ້ (U+0EC9), ຳ (U+0EB3): the tone mark comes before ຳ.
- A tone mark goes after the vowel sign (ກິ່ນ), never before it.
- Never insert a space, ZWSP, or line break between a prefixed vowel and its consonant, or between a consonant and its marks.

## 3. Normalization

- **NFC is safe.** It leaves Lao text unchanged (verified).
- **Do not apply NFKC (or NFKD) to Lao.** It rewrites ໜ to ຫ+ນ, ໝ to ຫ+ມ, and ຳ (U+0EB3) to ໍ+າ (U+0ECD U+0EB2) (verified). The result looks similar but is different data and breaks matching. Some search, database and text-cleaning pipelines apply NFKC by default; turn it off for Lao.
- **Variant spellings are not equivalent in Unicode:** ໜ / ຫນ, ໝ / ຫມ, ຫຼ / ຫລ. Pick one form per document (the modern forms ໜ ໝ ຫຼ unless the user's text uses the others) and keep it. Do not "normalize" a user's spelling unasked.

## 4. Invisible characters

| Code | Name | Use |
|---|---|---|
| U+200B | Zero-width space | Allowed line-break point between phrases or words. Never inside a syllable. Remove it from text that will be searched, copied, or counted. |
| U+2060 | Word joiner | Forbids a break (keeps a name together). |
| U+200C, U+200D | ZWNJ, ZWJ | Not needed for Lao. Remove them. |
| U+FEFF | BOM / ZWNBSP | Allowed once at the start of a UTF-8 file; stray ones inside text are bugs. |

## 5. Counting, matching, cutting

- `len(s)` counts code points, not letters or syllables.
- Match Lao with `[຀-໿]`; match Thai with `[฀-๿]`.
- Lao has no spaces between words. Use a dictionary-based segmenter for words: ICU `BreakIterator` for `lo` (PyICU, Java, ICU4C), or `new Intl.Segmenter("lo", {granularity: "word"})` in JavaScript.
- Grapheme segmentation (UAX #29, `regex.findall(r"\X", s)`, `Intl.Segmenter` with `grapheme`) keeps marks with their consonant, but **it does not bind a prefixed vowel to the consonant after it.** Cutting at a grapheme boundary can still strand ເ ແ ໂ ໄ ໃ at the end of a line. Use this helper to truncate (tested):

```python
import unicodedata

PREFIXED = range(0x0EC0, 0x0EC5)

def truncate_lao(s: str, limit: int) -> str:
    """Cut s to at most `limit` code points without stranding a prefixed vowel,
    or separating a mark, ະ າ ຳ ໆ or a zero-width character from its consonant."""
    cut = min(limit, len(s))
    def unsafe(i):
        if i <= 0 or i >= len(s):
            return False
        return (unicodedata.category(s[i]) in ("Mn", "Mc") or s[i] in "ະາຳໆ​⁠"
                or ord(s[i - 1]) in PREFIXED)
    while cut > 0 and unsafe(cut):
        cut -= 1
    return s[:cut]
```

When the cut falls inside the first syllable it returns an empty string; prefer cutting at a word or phrase break from the ICU segmenter.

## 6. Thai look-alike slips (common in AI-written text)

| Lao | Thai twin (wrong in Lao text) |
|---|---|
| ະ U+0EB0, າ U+0EB2, ຳ U+0EB3 | ะ U+0E30, า U+0E32, ำ U+0E33 |
| ເ ແ ໂ ໄ ໃ U+0EC0–0EC4 | เ แ โ ไ ใ U+0E40–0E44 |
| ່ ້ U+0EC8, U+0EC9 | ่ ้ U+0E48, U+0E49 |
| ໐–໙ U+0ED0–0ED9 | ๐–๙ U+0E50–0E59 |

`scripts/lao_check.py` reports a word that mixes both scripts (LAO001). Thai in its own words or blocks is fine when the document is bilingual.

## 7. Files and platforms

- Save as UTF-8. Excel opens a UTF-8 CSV with Lao correctly only when it starts with a BOM: write with `encoding="utf-8-sig"`.
- JSON: `json.dump(obj, f, ensure_ascii=False)` keeps Lao readable.
- HTML: `<meta charset="utf-8">` and `lang="lo"`.
- Keep file names and paths ASCII. Put Lao inside the file, not in its name.
- A terminal or console may show boxes or scrambled marks even when the data is correct. Judge by codepoints: `python3 -c "import sys,unicodedata as u; [print('U+%04X'%ord(c), u.name(c,'?')) for c in sys.argv[1]]" "ກິ່ນ"`.
- Text copied out of a PDF can lose marks or reorder prefixed vowels. Treat extracted text as unverified.

## 8. Legacy encodings

Old Lao files may use legacy fonts that put Lao shapes on Latin or private-use codes (U+E000–U+F8FF). Without the font the text is Latin gibberish or boxes. Do not guess a mapping: identify the font, find a converter for that exact font, convert, then run `scripts/lao_check.py`. Phetsarath OT, Noto Sans Lao and Noto Serif Lao are real Unicode fonts.
