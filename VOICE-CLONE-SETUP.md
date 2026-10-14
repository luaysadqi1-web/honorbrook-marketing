# Clone Luay's voice for the videos (ElevenLabs Instant Voice Clone)

Only Luay can do steps 1 to 4: they involve his account, payment and consent to clone his own voice. Steps 5 and 6 are mine.

## 1. Account and plan (Luay)
Sign up at elevenlabs.io with your own email and pick a paid plan. Starter includes the commercial license and Instant Voice Cloning (pricing page: $6 list, $1 promo shown; it contradicts itself, so confirm at checkout). Two videos use about 3,000 characters per full render, and re-renders reuse saved audio, so Starter's credits go a long way.

## 2. Record the sample (Luay, about 90 seconds)
- iPhone Voice Memos, phone 15 to 30 cm from your mouth, slightly to the side, in a quiet room with soft surfaces (closet, bedroom). No music, fan, or other voices.
- Read the paragraph below once, at the pace and warmth you would use with a client. Keep the tone and distance steady the whole way. ElevenLabs recommends 1 to 2 minutes, never more than 3.
- Send it to your Mac (AirDrop). If ElevenLabs rejects the .m4a file, tell me and I will convert it.

> Two years without Medicare drug coverage can add about nine dollars and forty cents a month to your premium, for as long as you have drug coverage. The clock starts when your Initial Enrollment Period ends. If you go sixty-three days in a row without Part D, or other creditable drug coverage, the late enrollment penalty can apply. It is one percent of the national base premium, thirty-eight ninety-nine in twenty twenty-six, times each full month without coverage. Six months comes to about two dollars and thirty cents a month. A year, four dollars and seventy cents. Two years, nine dollars and forty cents. It is added to your plan premium, and it follows you if you switch plans. To avoid it, enroll when you are first eligible, keep your creditable coverage notices, and do not let a gap reach sixty-three days. And ask about Extra Help. If you get it, you do not pay the penalty. Questions about your situation? Call five seven one, three five four, zero one four six. A licensed agent will reach out.

## 3. Create the clone (Luay)
Voices, then the plus icon, then **Instant Voice Clone**. Upload the recording, name it "Luay Sadqi (Honorbrook)", tick the consent statement ("the right and consent to clone the voice"), and click **Save voice**.

## 4. Give me access without pasting secrets in chat (Luay)
Copy the **API key** (ElevenLabs profile, API keys; limit it to text-to-speech if the page offers that), then run this in Terminal. It stores the key in a private file and never shows it:

```bash
mkdir -p ~/.config/honorbrook && pbpaste > ~/.config/honorbrook/elevenlabs.key && chmod 600 ~/.config/honorbrook/elevenlabs.key
```

Then copy the clone's **Voice ID** (My Voices, the clone's menu, Copy Voice ID) and run:

```bash
pbpaste > ~/.config/honorbrook/elevenlabs.voice
```

Then tell me it is done. Never paste the API key into chat.

## 5. Render (me)
```bash
VIDEO_VOICE_ENGINE=elevenlabs python3 scripts/video_studio.py build part-d
VIDEO_VOICE_ENGINE=elevenlabs python3 scripts/video_studio.py build aca
python3 scripts/video_studio.py embed part-d && python3 scripts/video_studio.py embed aca   # refresh transcript and length on the pages
```
Tuning knobs if the first render sounds off: `EL_STABILITY` (lower is more expressive, default 0.5), `EL_SIMILARITY` (default 0.8), `EL_SPEED` (default 1.0), `ELEVENLABS_MODEL` (default `eleven_multilingual_v2`). Each tweak re-bills only the lines that changed.

## 6. Rules for using the clone
- Videos only. Do not use it on phone calls or voicemail: the FCC treats AI voices in calls as artificial under the robocall rules (2024 ruling; confirm with counsel).
- The video end card automatically says "Narration: AI voice cloned from Luay Sadqi's own voice, with his permission." Keep a matching line in each post's description, and switch on TikTok's and Instagram's AI-content label when you upload.
- YouTube's help page lists cloning your own voice for voice-overs as not needing a disclosure, but the note is harmless.
- Never clone or imitate anyone else's voice. ElevenLabs also blocks cloning other people.
- Check with your carriers' compliance before posting Medicare videos with an AI voice. I found no CMS rule on AI voices in my research, but carriers often review agent marketing.
- Delete the API key file (`rm ~/.config/honorbrook/elevenlabs.key`) and revoke the key in ElevenLabs if you stop using it.

## Backup: Luay's real recording
If you would rather speak the whole video yourself, record the read-aloud lines in `VIDEO-VOICE-MUSIC-RESEARCH.md` with a clear one-second pause between lines, then run `VIDEO_VOICE_ENGINE=recorded VIDEO_RECORDED_FILE=/path/to/recording.m4a python3 scripts/video_studio.py build part-d`. The builder splits the recording at the pauses and times the animation to your delivery.
