# Better videos: human voice, background music, and what else moves the needle

Research done Oct 14, 2026. "Verified" means I read the provider's own page or the regulation text this session. "Secondary" means a vendor blog or news piece; treat those as directional. Nothing here has been published or bought.

## Bottom line
1. **Use Luay's real voice.** It is free, it is the trust signal the earlier strategy asked for, and it avoids every AI-voice labeling question. Two phone recordings (about 70 and 85 seconds of speech) are enough for me to rebuild both videos around it.
2. **Add a quiet licensed music bed, mixed 15 to 20 dB under the voice and ducked while he speaks.** Mixkit's free license covers online marketing ads and social posts (verified). The music in the current videos is a generated pad that is licensing-safe but generic.
3. **If he will not record every video, clone his own voice** (ElevenLabs Instant clone, own voice only) rather than using a stock AI voice. Or pay a human voice actor (roughly $100 to $500 per 60-second spot, secondary sources).
4. **Fix one compliance gap before posting more Medicare video** (see "Flag" below).

## Voice options
| Option | How it sounds | Cost | Rights, consent, labels | Verdict |
|---|---|---|---|---|
| **Luay records on iPhone** (Voice Memos, "Enhance Recording," 15 to 30 cm from the mouth, soft room) | Real, trusted | $0 | None | **Best.** Optional cleanup: Adobe Podcast Enhance Speech (free, browser), Auphonic loudness leveling (free tier about 2 h/month, secondary) |
| **ElevenLabs Instant Voice Clone of Luay** | Close to him; fast | Plans with commercial license: Starter $6/mo list ($1 promo shown), Creator $22/mo list ($11 promo shown). The pricing page contradicts itself, so confirm at checkout | Own voice only; Instant needs 1 to 2 minutes of audio. YouTube's help page says cloning your own voice for voice-overs needs no disclosure (verified). TikTok asks creators to label realistic AI audio and video (secondary; I did not open TikTok's policy) | Good backup. Still disclose in the description to be safe |
| ElevenLabs Professional clone | Near-identical | Creator plan or above | Must pass a voice verification; 30 to 180 minutes of audio | Overkill for now |
| ElevenLabs / Google Chirp 3 HD / Azure stock voices | Natural, but a stranger | ElevenLabs is the priciest. Google about $30 per million characters, Azure about $16 (secondary, sources conflict). One of our videos is about 1,300 characters, so cost is cents | Commercial terms differ by plan; check each | Fine for drafts, weak on trust |
| OpenAI gpt-4o-mini-tts (13 voices, steerable tone, speed and whispering) | Natural, a bit flat on emotion (secondary) | About $15 per million characters (secondary) | **Usage policy requires telling listeners the voice is AI-generated** (verified) | Cheap, but forces an on-screen AI disclosure |
| Hire a human voice actor | Real, polished | About $100 to $500 per 60 seconds with online usage rights; broadcast and union cost far more (secondary) | Get usage rights, term and paid-media use in writing | Good if Luay will not record |
| macOS Premium voices (free download in System Settings > Accessibility > Spoken Content) | Better than now, still synthetic | $0 | None | Quick upgrade; **this Mac has no Premium voices installed**, so the videos use a basic one |
| Apple Personal Voice | Robotic per reviews | $0 | Nothing I found says it can be exported to a file | Skip |
| Local open models: **Kokoro-82M** (Apache 2.0, 54 voices, no cloning), **Chatterbox** (MIT, clones from a reference clip, watermarks output) | Good to very good | $0 | Licenses verified on the model pages. Avoid F5-TTS weights (non-commercial) | Kokoro needs its Python package plus the espeak-ng tool (verified); it likely needs a newer Python than this Mac's 3.9 (not confirmed). This Mac has no Homebrew or uv, so I need your OK to install anything |

**Why not ship the stock AI voice:** the strategy doc already judged "computer voice over slides" as the main reason videos get ignored. A stranger's AI voice has the same problem.

## Background music
**What is safe to use, by source**
| Source | License facts | Verdict |
|---|---|---|
| **Mixkit Stock Music Free License** | Allowed: podcasts, social media video posts, online marketing ads, educational use, YouTube. Not allowed: CDs/DVDs, TV and radio broadcasts, video games. You may not register tracks with a rights-management service (verified, license page) | **Best free choice.** Save a screenshot of each track's license |
| Uppbeat | Pro tier covers digital ads and client content; listed at $17.99/mo (Uppbeat's own page; figures conflict between its pages; the pricing page returned an error when I tried it) | Good paid option; rights end for new uploads if you cancel |
| ElevenLabs Music (AI-generated instrumentals) | Self-serve plans allow online and offline commercial use except film, TV and Studio Games; Free is personal only (verified, product page). The page says built "in partnership with artists, labels, and publishers" but does not state its training data | Workable; keep plan and date records |
| Pixabay | Content License: free, no attribution, commercial use allowed with limits. Its summary does not address ads or music specifically, and it disclaims third-party rights (verified) | Usable, but read the track's page; Content ID claims are possible (secondary) |
| YouTube Audio Library | "Copyright-safe" for videos on YouTube; some tracks require credit; the page says nothing on use in ads or on other platforms (verified) | Fine for YouTube-only posts |
| Meta Sound Collection | Commercial use allowed **only inside Meta products**, including Ads Manager; using the audio separately is not licensed (verified from the terms snippet) | Use inside Instagram/Facebook tools, not baked into files used elsewhere |
| TikTok Commercial Music Library | Business accounts are steered here; license covers TikTok only (secondary; I did not open TikTok's terms) | TikTok-only |
| Suno | Free tier: no commercial use. Paid: sources disagree on ownership (secondary) | Avoid for ads |
| Udio | A Sept 2026 review says downloads are off (secondary) | Avoid |
| Popular songs, "trending sounds" | Business accounts lose consumer libraries and trending audio is generally not cleared for ads (secondary) | Never |

**Mix targets** (guides, not standards): put music 15 to 20 dB below the voice while he speaks (one guide says 15 to 25), with a 10 to 30 ms attack and 200 to 500 ms release on the ducking, and let it rise slightly in pauses. YouTube normalizes playback to about -14 LUFS, so do not master louder than that. I found no official Instagram loudness target. Check on phone speakers and earbuds. Right now my mix has a fixed quiet pad, not true ducking; I can add ducking once there is a voice track.

## Compliance for AI voice and visuals
- **YouTube** (verified help page): disclose realistic content that makes a real person appear to say something they did not. Own-voice cloning for voice-overs, audio repair, captions and script help are listed as not needing disclosure. A stock AI narrator is not addressed by name.
- **New York synthetic performer law** (secondary, law-firm summaries): in effect June 9, 2026; covers AI-generated visual or audiovisual "performers" in ads; **audio-only ads are excluded**; no prescribed wording; $1,000 first and $5,000 later violations. Our videos have no performer. An AI talking avatar would be in scope; have counsel check before using one.
- **CMS** (verified, 42 CFR 422.2267): the third-party marketing organization disclaimer must be included in marketing materials, including print and television advertisements. The "read it at the same pace as the phone number, or show it in the same font size" test appears in the text I read for another disclaimer (e)(34)(iv); I could not confirm whether it also governs the TPMO disclaimer in video. Secondary sources say CMS bars AI deepfakes of public figures in marketing; I did not find that text. The earlier note that the rule has no AI-specific video requirement still stands as unverified.
- Platform labels: TikTok labels via C2PA metadata and creator disclosure; Meta's approach was not confirmed from an official page (secondary).

### Flag: our Medicare disclaimer text looks out of date
The eCFR text for 42 CFR 422.2267(e)(41) (current as of Oct 2026, read via the eCFR API and Cornell LII) gives the disclaimer as: "We do not offer every plan available in your area. Currently we represent [number] organizations which offer [number] products in your area. Please contact Medicare.gov or 1-800-MEDICARE to get information on all of your options."

The site uses a different sentence in 1,162 pages, including the video end cards: "Any information we provide is limited to those plans we do offer in your area." and has the "Currently we represent..." sentence on none. I did not change anything. This needs your carriers' or FMO's compliance team, and it needs the real counts (organizations and products) for the areas you serve. Do not rely on my reading alone.

## Making the videos better beyond audio
Done already: hook with the payoff first, word-by-word captions, vertical 9:16 masters, motion graphics tied to the narration, source line on screen, Virginia's date fixed.

Next, in order of lift:
1. **Luay's voice, then Luay on camera** for 30 to 60 second vertical clips (one question each, answer in the first sentence). Secondary guides agree the first three seconds decide whether people stay.
2. **Cut-downs.** Our videos run 70 and 83 seconds. Make 30 to 40 second versions for Shorts and Reels (for Part D: hook, the 63-day grid, how to avoid it). Guides say to stop at the shortest length that answers the question.
3. **Publish to YouTube first**, embed it at the top of the matching post, then post Shorts and Reels. Add GA4 events for video play and form submit so you can see which post produces calls.
4. Keep captions on every video; many viewers watch muted (the commonly quoted 85% figure is not traceable to a primary source).
5. Insurance-specific engagement numbers circulating online come from vendor blogs with no source; I would not quote them.

## Decisions for you
1. Will Luay record his own voice? If yes, I will send read-aloud scripts (below) and rebuild once I have the audio.
2. If not, clone his voice (needs his account and consent) or hire talent?
3. Music: free Mixkit track, or a paid library for more choice?
4. OK to install Python and speech tools on this Mac, or stay with what is already here?
5. Who confirms the Medicare disclaimer wording and counts with your carriers?

## Read-aloud scripts (Luay's voice)
Read each line as its own take with a short pause between lines; the video follows his pacing.

**Part D late penalty**
- Two years without Medicare drug coverage can add about nine dollars and forty cents a month to your premium.
- For as long as you have drug coverage.
- The clock starts when your Initial Enrollment Period ends.
- Go sixty-three days in a row without Part D, or other creditable drug coverage,
- and the late enrollment penalty can apply.
- One percent of the national base premium, thirty-eight ninety-nine in twenty twenty-six,
- times each full month without coverage.
- Six months, about two dollars and thirty cents a month.
- A year, four dollars and seventy cents.
- Two years, nine dollars and forty cents.
- Three years, fourteen dollars.
- It is added to your plan premium.
- And it follows you if you switch plans.
- To avoid it, enroll when you are first eligible.
- Keep your creditable coverage notices.
- Do not let a gap reach sixty-three days.
- And ask about Extra Help. If you get it, you do not pay the penalty.
- Questions about your situation? Call five seven one, three five four, zero one four six, or fill out the form at honorbrook-insurance dot com.
- A licensed agent will reach out.

**ACA plan comparison:** the same, using the caption lines in `scripts/video_studio.py` (`ACA`).

## Sources read directly
[YouTube help: disclosing altered or synthetic content](https://support.google.com/youtube/answer/14328491) · [OpenAI text-to-speech guide](https://developers.openai.com/api/docs/guides/text-to-speech) · [ElevenLabs voice cloning docs](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning) · [ElevenLabs pricing](https://elevenlabs.io/pricing) · [ElevenLabs Music](https://elevenlabs.io/music) · [Pixabay terms](https://pixabay.com/service/terms/) · [Mixkit stock music license](https://mixkit.co/license/modal/musicFree/) · [YouTube Audio Library help](https://support.google.com/youtube/answer/3376882) · [Meta Sound Collection terms](https://www.facebook.com/sound/collection/terms) (search snippet) · [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) · [Chatterbox](https://github.com/resemble-ai/chatterbox) · [42 CFR 422.2267](https://www.law.cornell.edu/cfr/text/42/422.2267) · [New York synthetic performer law summary](https://www.hunton.com/privacy-and-cybersecurity-law-blog/new-york-enacts-law-regulating-the-use-of-ai-generated-synthetic-performers-in-advertising)

## Not verified
Uppbeat free-tier terms; TikTok's own music and AI-label pages; Artlist and Epidemic Sound prices and ad coverage; Descript features; whisper.cpp and WhisperKit word-timing quality; whether the New York law reaches an agency not licensed in New York; the exact CMS rule for video ads.
