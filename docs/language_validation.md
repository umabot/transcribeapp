# Language Support Guide

This project currently implements three transcription providers with language validation:

- **AWS Transcribe**
- **GCP Speech-to-Text**
- **Local Whisper**

The accepted language format depends on the provider:

| Provider | Format required | Examples | Regional variants |
| -------- | --------------- | -------- | ----------------- |
| AWS | BCP-47 | `en-US`, `fr-FR`, `es-ES` | Yes |
| GCP | BCP-47 | `en-GB`, `pt-BR`, `zh-CN` | Yes |
| Whisper | ISO 639-1 | `en`, `fr`, `es` | No |

## Important rules

### AWS and GCP

Cloud providers require **BCP-47** codes in the form:

- `language-REGION`
- examples: `en-US`, `fr-FR`, `de-DE`

These will be normalized automatically if the case is wrong:

- `EN-us` → `en-US`
- `fr-fr` → `fr-FR`

Using only `fr` or `en` with AWS or GCP will fail validation.

### Whisper

Whisper requires **ISO 639-1** two-letter codes:

- `en`, `fr`, `es`, `de`, `ja`, `zh`

These are normalized to lowercase:

- `EN` → `en`
- `Fr` → `fr`

Using `en-US` or `fr-FR` with Whisper will fail validation.

---

## AWS Transcribe languages

Use AWS when you want cloud transcription with BCP-47 regional language codes.

### AWS examples

- English: `en-US`, `en-GB`, `en-AU`, `en-IN`, `en-IE`, `en-AB`, `en-WL`, `en-ZA`
- Spanish: `es-ES`, `es-US`, `es-MX`
- French: `fr-FR`, `fr-CA`
- German: `de-DE`, `de-CH`
- Portuguese: `pt-BR`, `pt-PT`
- Chinese: `zh-CN`, `zh-TW`
- Arabic: `ar-SA`, `ar-AE`

### Additional AWS-supported codes in this implementation

`af-ZA`, `cs-CZ`, `da-DK`, `el-GR`, `fi-FI`, `he-IL`, `hi-IN`, `hu-HU`, `id-ID`, `it-IT`, `ja-JP`, `ko-KR`, `ms-MY`, `nl-NL`, `no-NO`, `pl-PL`, `ro-RO`, `ru-RU`, `sv-SE`, `ta-IN`, `te-IN`, `th-TH`, `tr-TR`, `uk-UA`, `vi-VN`

### AWS notes

- Omit the language option to allow AWS language auto-detection.
- If you specify a language, it must be one of the values accepted by the validator.

---

## GCP Speech-to-Text languages

Use GCP when you want cloud transcription with broad regional language coverage.

### GCP examples

- English: `en-US`, `en-GB`, `en-AU`, `en-IN`, `en-CA`, `en-NZ`, `en-SG`, `en-ZA`
- Spanish: `es-ES`, `es-US`, `es-MX`, `es-AR`, `es-CL`, `es-CO`
- French: `fr-FR`, `fr-CA`, `fr-BE`, `fr-CH`
- German: `de-DE`, `de-AT`, `de-CH`
- Portuguese: `pt-BR`, `pt-PT`
- Chinese: `zh-CN`, `zh-TW`, `zh-HK`
- Arabic: `ar-SA`, `ar-EG`, `ar-AE`, `ar-MA`

### Additional GCP-supported codes in this implementation

`bg-BG`, `bn-IN`, `ca-ES`, `cs-CZ`, `el-GR`, `eu-ES`, `fil-PH`, `fi-FI`, `gl-ES`, `gu-IN`, `he-IL`, `hi-IN`, `hr-HR`, `hu-HU`, `id-ID`, `it-IT`, `ja-JP`, `kn-IN`, `ko-KR`, `ml-IN`, `mr-IN`, `ms-MY`, `nb-NO`, `nl-BE`, `nl-NL`, `pl-PL`, `ro-RO`, `ru-RU`, `sk-SK`, `sl-SI`, `sv-SE`, `ta-IN`, `te-IN`, `th-TH`, `tr-TR`, `uk-UA`, `vi-VN`

### GCP notes

- Omit the language option to let the GCP flow use its built-in fallback and alternative language handling.
- GCP accepts more regional variants than AWS in the current implementation.

---

## Whisper languages

Use Whisper when you want local transcription and simpler language codes.

### Whisper examples

`en`, `es`, `fr`, `de`, `it`, `pt`, `nl`, `ja`, `ko`, `zh`, `ar`, `hi`, `ru`

### Supported Whisper codes in this implementation

`af`, `am`, `ar`, `az`, `be`, `bg`, `bn`, `bs`, `ca`, `ceb`, `co`, `cs`, `cy`, `da`, `de`, `el`, `en`, `es`, `et`, `eu`, `fa`, `fi`, `fr`, `ga`, `gd`, `gu`, `haw`, `he`, `hi`, `hmn`, `hr`, `ht`, `hu`, `hy`, `id`, `ig`, `is`, `it`, `ja`, `jw`, `kk`, `km`, `kn`, `ko`, `la`, `lb`, `lo`, `lt`, `lv`, `mg`, `mi`, `mk`, `ml`, `mn`, `mr`, `ms`, `mt`, `my`, `ne`, `nl`, `no`, `ny`, `pa`, `pl`, `ps`, `pt`, `ro`, `ru`, `sd`, `si`, `sk`, `sl`, `sm`, `sn`, `so`, `sq`, `sr`, `st`, `su`, `sv`, `sw`, `ta`, `te`, `tg`, `th`, `tl`, `tr`, `tt`, `uk`, `ur`, `uz`, `vi`, `xh`, `yi`, `yo`, `zh`, `zu`

### Whisper notes

- Omit the language option to let Whisper auto-detect the language.
- Whisper does **not** use region-specific codes such as `en-US` or `fr-CA`.

---

## Correct and incorrect examples

| Goal | Correct | Incorrect |
| ---- | ------- | --------- |
| AWS French | `fr-FR` | `fr` |
| GCP English | `en-US` | `en` |
| Whisper English | `en` | `en-US` |
| Whisper French | `fr` | `fr-FR` |

## Practical CLI examples

```bash
python3 ./scripts/mytranscript.py input.wav output.md --provider aws --language en-US
python3 ./scripts/mytranscript.py input.wav output.md --provider gcp --language fr-FR
python3 ./scripts/mytranscript.py input.wav output.md --provider local --language en
```

## Source of truth

The language sets documented here reflect the validation logic currently implemented in:

- `src/validation/language.py`

If new languages are added to the code, this document should be updated to match.
