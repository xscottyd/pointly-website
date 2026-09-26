---
title: "Pointly — Beta Tester Guide"
permalink: /tester-guide.html
---

# Pointly — tester guide

**Version under test:** 1.1.0

**Get it:** https://play.google.com/store/apps/details?id=com.xscottyd.pointly

**Web:** https://play.google.com/apps/testing/com.xscottyd.pointly

**More about the app:** https://pointly.scottdavis.uk/

**Contact:** pointly-beta@scottdavis.uk


---

Pointly turns your Android phone into a point-and-tap remote for Home Assistant. Instead of
digging through dashboard cards or shouting at a voice assistant, you point the phone at a lamp,
a speaker or a switch, the screen tells you when it's locked on, and you tap to control it. It
talks directly to your own Home Assistant server using your own access token, teaches itself
where your devices are, and can stay scoped to the room you're standing in so you don't
accidentally fire the kitchen light from the sofa. It also carries a public demo home so you can
try it out, or test without Home Assistant.

Quick note: 
The "aim" is only saved from a single position. So if you set everything up when you're on the sofa, it may not work when you move to say, the arm chair, if the aim position is different

---

## Before you start

You'll need:

- An **Android phone** (Android 12 or newer). It must have a **compass/rotation sensor**
- About **20 minutes**.
- Optionally your Home Assistant details (Step 1 will tell you whether you need them).


---

## Step 1 — Do you want to use your own Home Assistant, or the demo?

**This is the first decision, and it changes the rest of the test.**

### Option A — Use your own Home Assistant *(more useful test)*

Choose this if you run Home Assistant and have real devices you don't mind toggling.

- You need your Home Assistant address (the URL you use in a browser, e.g.
  `http://192.168.1.50:8123`). **Use the local IP address**, not a `.local` address — those are
  unreliable on some Android phones.
- You need a **long-lived access token**: in Home Assistant, click your name → **Security** →
  **Long-Lived Access Tokens** → **Create Token**. Copy it and keep it somewhere safe.
- **Your phone must be on the same network as your Home Assistant.**
- ⚠️ **Pointly will control real devices in your home.** Nothing happens until you tap, and
  nothing gets taught until you teach it — but it will be genuinely switching your lights.

This path is worth doing if you can, because it's the only way to find out how Pointly behaves
with your actual setup, your actual room setup, and your real device types.

### Option B — Use the demo home *(quickest, zero setup)*

Choose this if you don't have Home Assistant, or want a look before committing to your own.

- The demo is a public Home Assistant we host, with 26 fake devices: lights, switches, a media
  player, a thermostat, a garage door, a person tracker and more.
- It behaves like a real Home Assistant: your taps really do change the device state and the
  change comes back live. **Nothing is fake in the interaction** — only the house is.
- The demo is **shared with other testers** and its state resets when the server restarts. Treat
  it as a sandbox: don't put anything personal in it.

**If you're not sure:** do Option B first to decide whether you like the idea, then Option A if
you want to go deeper. You can switch at any time from the Home Assistant connection screen.

---

## Step 2 — Install and open it

1. Install from the link at the top of this document.
2. Open **Pointly**.
3. You'll land on the connection screen asking for a **Home Assistant URL** and a
   **long-lived access token**.

### If you chose Option A

Fill in your own URL and token, tap **Validate**, and let it check. If it can't reach your
server, it will tell you — most often it's a wrong URL, a wrong network, or a token that hasn't
finished being created. There's a **Skip SSL verification** option if your Home Assistant uses
a self-signed certificate.

Next it asks **which room you're in**. It offers two routes:

- **Pick a Home Assistant room entity** — Pointly reads the current room from an entity
  (something like an `input_select` or a room-occupancy helper). This is the more automatic
  option, and it's worth doing if you have such an entity.
- **Or manage rooms in this app instead** — Pointly will ask you to pick the room yourself, on
  the app's own screen, every time. Simpler, no HA setup.

**If you're testing room-scoping at all, set your rooms up before you teach any devices** —
rooms and teaching are linked, and it's much less work to teach in the right room than to fix it
afterwards.

### If you chose Option B

On that same connection screen, **press and hold the screen title for 5 seconds**. The demo
server's address and token fill themselves in and it connects on its own. (This is deliberately
a hidden gesture so nobody configures a demo server by accident — but you're a tester, so here
it is.)

If nothing happens, keep holding — it genuinely needs a full 5 seconds and it will feel like
nothing is going on for a while.


---

## Step 3 — The test tasks

Work through these in any order. **Note anything that surprises you** — good or bad. A task that
"worked fine" is useful, but the interesting feedback is the awkward edges.

### Getting set up

-  **Teach your first device.** Long-press the big button on the home screen, pick a device from the list, aim at it, and save where it is.
-  **Teach a second and third device.** Ideally not too close together, but try it and see what fustrates you!
-  **Toggle each of them.** Check the state actually changed, and that it changes back.
-  **Delete one of them** and tell us how hard that was to find.

### The core interaction

-  **Try to lock onto a device from across the room.**
-  **Try to pick out one device from a tight cluster** (two bulbs next to each other).
-  **Deliberately point at nothing** and see what happens.
-  **Move your phone fast, then slowly**, and compare how it behaves.
-  **Point at a device, then walk away and come back** — does it still know what you meant?
-  **Point at a different device while one is already matched** — does it hand over cleanly?

### Room awareness

-  **Switch rooms** (swipe on the screen left or right, or tap the room name to pick).
-  **Add a room.** Give it a name.
-  **Rename a room.**
-  **Delete a room** that has a device in it, and see what happens to that device.
-  *(Option A only)* **Import your rooms from Home Assistant areas** instead of typing them.
-  *(Option A only)* If you have a room-occupancy entity, **switch to using it** and see
      whether the app follows you around the house.

### Context controls

-  **Adjust brightness** on a light that supports it.
-  **Adjust volume** on a media player.
-  **Try the media buttons** (play, pause, skip) where available.
-  **Open the panel on a device that has no extra controls** and see whether that's confusing
      or fine.

### Hot buttons (custom one-tap actions)

-  **Add a hot button** to a device — pick a service, fill in the fields, give it a name, save.
-  **Test-fire the action before saving it.**
-  **Edit it** afterwards.
-  **Delete it.**
-  **Add two or three hot buttons to the same device** and check they're all reachable.
-  **Create one for a scene or script** rather than a plain on/off (Option B has "Movie Night" and "Goodnight" to try).

### Settings

-  **Change the accent colour** — try a preset, then a custom colour.
-  **Change the global sensitivity**, then go back and try pointing again.
-  **Change the sensitivity for one single device** so it differs from the global setting.
-  **Turn on "sticky match"** for a device you use a lot, then point at it, look away, and keep using it. Then point at a *different* device and see if it releases properly.
-  **Re-aim or rename a taught device.**
-  **Open Help** from the home screen and tell us whether it answered your questions.
-  **Open the debug readout** (long-press the cog) and have a look.

### Ads

*(Skip this section if you don't see any adverts — you may well not.)*

- **Find the advert** (there's a banner on the Settings screen, and one in the debug readout).
- **Tell us what you think of it** — did it get in the way?


---

## Step 4 — Rate it

Score each out of 5. Be blunt, this doesn't help anyone if it's polite.

| Area | 1–5 | Anything to add |
|---|---|---|
| Getting set up | | |
| Pointing at the right device (accuracy) | | |
| Speed of response | | |
| Room awareness | | |
| Context controls / hot buttons | | |
| How it looks and feels | | |
| Overall | | |

And three questions:

1. **Would you use this daily?** Yes / No / Maybe — and why.
2. **What's the first thing that confused you?**
3. **If you could change one thing, what would it be?**

---

## If something goes wrong

That's useful data, not a failed test — please still tell us.

Useful to include:

- Your **phone model** and **Android version** (Settings → About phone).
- **Which option you chose** (your own Home Assistant, or the demo).
- **Which step you were on** and what you did.
- **What you expected** and **what happened** instead.
- A photo or screenshot is gold if you hit something visual.

One thing worth knowing: if the pointer feels like it drifts or is jumpy, waving the phone in a
figure-of-eight recalibrates the compass on most phones. If that fixes it, tell us — that's
worth knowing, because it affects how we'd explain the app.

---

## Thank you

This app is built by one person in spare time, and every piece of feedback — including the
critical kind — genuinely changes what gets built next.
