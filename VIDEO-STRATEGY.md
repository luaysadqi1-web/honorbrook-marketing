# Video strategy: tools, skills and rules (researched Oct 14, 2026)

## Why the first two videos won't get watched
(My assessment, not measured data. We have no view counts yet.)
- Computer-generated voice over text slides: no face, no trust. Insurance is a trust purchase.
- Buried mid-page, click-to-play, no hook in the first 3 seconds, 60-83 seconds long.
- Hosted only on our own site. Nothing is distributed on YouTube, Shorts, Reels, TikTok or Facebook.

## What to change (in priority order)
1. **Put Luay on camera.** 30-60 second vertical clips (1080x1920), one question per clip, answer in the first sentence, spoken to the phone camera. Same questions as the blog titles. This is the single biggest lift.
2. **Publish to YouTube first** (Shorts plus a few long-form), then embed the YouTube video on the matching blog page. Google says YouTube-hosted videos get key moments from timestamps in the description (developers.google.com/search/docs/appearance/structured-data/video). Long-form tends to win search and AI citations; Shorts are for discovery (seo.com, directional).
3. **Move the video to the top of each post**, under the answer paragraph, with a hook title.
4. Add `Clip` or `SeekToAction` markup only for self-hosted videos of 30 seconds or more.

## Tools, grouped by job

### A. Edit footage Luay films (best return)
| Tool | What it does | Notes |
|---|---|---|
| **IT Reelsmaker** (Claude plugin, community) | Cuts pauses and retakes, word-timed subtitles, branded motion graphics in Remotion, 1080x1920 render | Runs locally; needs ffmpeg + Node + Python. This Mac has none of ffmpeg or Node installed. |
| **Video Cleanup** (Claude plugin, community) | AI noise removal, loudness, picture fixes, logo watermark, name lower third, end card | Needs Python + ffmpeg. |
| **BlitzReels** (Claude plugin, hosted) | Editing, clipping long videos into shorts, carousels | Needs a BlitzReels account. |
| **Descript / Captions / CapCut** | Transcript-based editing, auto-captions | Consumer apps; Captions' voice cloning is limited per reviews. |
| **Adobe for creativity** and **Canva** plugins (already in your environment) | Quick cuts, resize one video for every social format, brand kit | Adobe needs sign-in authorization. |

### B. AI presenter / avatar (scale without filming each one)
| Tool | Notes |
|---|---|
| **HeyGen** | Most-cited for avatar + voice clone + captions + translation (vendor blogs, weigh accordingly). |
| **Synthesia** | Stronger for training and enterprise controls. |
| **ManyMotions "AI Avatar Presenter"** (Claude plugin, hosted) | Lets me script and render from here. Needs a ManyMotions account. |
| Pricing | Sources conflict (roughly $18-29/month entry plans). Check each vendor's current page. |

**Rules for avatars:** only use Luay's own likeness and voice, with his consent. Label them as AI-generated. A synthetic Luay may convert worse than the real one. Check each platform's AI-content label rules before posting.

### C. Programmatic / data-driven videos
- **Remotion** (open-source React video framework; Claude agent skills exist) for branded animated explainers from data (rates, dates, deadlines). My current builder (`scripts/make_video.py`) is a simple version of this. Needs Node.

### D. Publishing and measuring
- **Postiz** skill and **Metricool** (already connected for Facebook and Instagram) to schedule posts.
- GA4 is on the site. Add events for video play and form-submit so we can see which posts convert.

## Compliance (from searches; confirm against CMS text)
- CMS requires the marketing organization's name to appear for the whole video ad in a comparable font size, or be read at the same pace as the phone number (per agent compliance summaries of the CMS rule).
- A video that names a specific plan, highlights specific benefits or includes an enrollment call-to-action is generally treated as marketing material the carrier must file with CMS (HPMS). **Keep videos educational: no plan names, no benefits, no "enroll now."**
- CY2027 CMS guidance reportedly removed SHIP from the disclaimer; use "Medicare.gov or 1-800-MEDICARE." The standard disclaimer is now on the three pages that had the old wording.
- End card on every video: name, "Honorbrook Insurance," "We do not offer every plan available in your area. Contact Medicare.gov or 1-800-MEDICARE for all of your options," phone and website.
- Never say "free" about plan costs, and never quote plan prices, returns or rates.
- Not verified here: the exact on-screen text CMS requires on a video itself. Confirm with your compliance source or the carrier.

## Proposed plan
1. Luay films 5 vertical clips from scripts I write (hook-first, question-led, compliant): Part D late penalty, ACA plan comparison, ACA at 65, TSP rollover, "do nothing during AEP."
2. Install ffmpeg + Node locally (needs your OK) so I can run IT Reelsmaker / Remotion and caption, brand and export each clip in vertical and landscape.
3. Upload to YouTube, embed on the matching posts at the top, post Shorts/Reels with Postiz or Metricool.
4. Add GA4 video-play and form-submit events. Review after 2 weeks.
