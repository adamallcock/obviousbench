---
title: ObviousBench Pro Consult Status
date: 2026-06-07
type: note
status: blocked
---

# ObviousBench Pro Consult Status

Attempted to consult ChatGPT Pro through the visible ChatGPT web UI using the
`chatgpt-browser-control` and `chatgpt-pro-consult` skill path.

## What Worked

- Chrome bridge doctor reported bridge and login as OK.
- Pro mode selection succeeded in new threads:
  - `Pro • Extended`
  - `Extended Pro`
- File attachment succeeded for both the full and slimmer file sets.
- A compact text-only Pro prompt submitted successfully.
- The compact consult thread URL is:
  `https://chatgpt.com/c/6a25d19d-57d4-83ea-a2f7-aa271eeb51d0`

## What Did Not Work

- The full file-backed consult attached files but the `ask` step timed out
  before an assistant turn appeared.
- The slimmer file-backed consult had the same pattern.
- The first text-only prompt was too long for composer verification and failed
  with `ComposerVerificationError`.
- The compact text-only prompt submitted successfully, but the visible assistant
  response remained incomplete after three bounded reads:

```text
I’ll approach this as launch positioning plus copy surgery. I’ll focus on sharpening the product-quality frame, avoiding overclaiming, and moving the split/release caveats earlier.
```

- A follow-up "continue" attempt in the same thread stopped because Pro mode
  selection returned `unsupported`; the automation did not continue in a
  non-Pro mode.

## Useful Partial Signal

Even the partial Pro response reinforces three local priorities:

- sharpen the product-quality frame;
- avoid overclaiming;
- move split/release caveats earlier.

## Next Retry Recommendation

Retry the Pro consult in a fresh turn with either:

1. one compact prompt under 6,000 characters and no attachments; or
2. a single combined context file instead of many separate attachments.

If using files, wait for file processing to settle before submitting, or use a
browser-control primitive that separates attach and submit with an explicit
post-attach wait.
