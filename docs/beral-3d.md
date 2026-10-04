# Beral 3D: model brief and integration notes

## Status

The app is ready for a rigged 3D Beral, but **the 3D model itself does not exist yet**. Until it is added, the app shows the four Beral pictures exactly as before. Nothing in the app pretends the pictures are 3D.

The missing production asset is **one rigged, animated GLB file of Beral**, made by a 3D artist from the four reference pictures in `public/static/mascot/` (`mascot_welcome.png`, `mascot_celebrate.png`, `mascot_encourage.png`, `mascot_thinking.png`).

## Where the model goes

Save the finished file as:

```
public/static/mascot/beral.glb
```

Then deploy. The app finds the file when it starts and switches to the 3D Beral by itself.

If the file is hosted somewhere else (for example a CDN), set `BERAL_MODEL_URL` in `.env` and in Vercel to its full address instead. That host must allow cross-origin requests from the app. If the 3D Beral does not appear on Vercel after adding the file, set `BERAL_MODEL_URL=/static/mascot/beral.glb` there as well.

Check the result at **Admin, Overview, Beral 3D preview** (`/admin/beral`). It lists every clip found in the file and every clip still missing, and has a button for each animation.

## What the 3D artist must deliver

### Look

- The same character as the pictures: young Black boy's face, short clean hair, white and black robotic armour, glowing blue lights, blue chest core, friendly expression, same proportions.
- Not a generic robot.
- No text in the model. Speech bubbles are made by the app.

### File

- Format: GLB (binary glTF 2.0), one file holding the mesh, skeleton, materials and all animation clips.
- Orientation: Y up, character facing +Z, feet at the origin, real world scale (about 1.4 to 1.7 units tall).
- Size budget: about 25,000 triangles or fewer, textures 1024 px (2048 px at most), file under 5 MB. Draco or meshopt compression (for example with `gltfpack -cc`) is supported. Use PNG, JPEG or WebP textures. KTX2 textures are not supported yet.
- Materials: standard PBR (metallic and roughness). Put the blue lights on materials with an **emissive** colour, so the app can pulse them gently while Beral is idle.
- One skinned mesh (or a few), with at most 4 bone influences per vertex.

### Skeleton

A humanoid rig with at least these joints. Mixamo or Unreal style names are fine:

| Area | Bones |
| --- | --- |
| Body | hips (root), spine, chest, neck, head |
| Each arm | shoulder (clavicle), upper arm, elbow (forearm), wrist, hand, simple finger bones for a thumbs up |
| Each leg | upper leg, knee (lower leg), ankle (foot), toe |

### Face (optional but recommended)

Morph targets (shape keys) with these exact names, from 0 (neutral) to 1 (full):

`Blink`, `Smile`, `MouthOpen`, `BrowsUp`, `BrowsDown`, `MouthSide`, `Thinking`

The app blinks with `Blink` every few seconds and blends the others for each mood. Any name that is missing is simply skipped.

### Animation clips

Clip names matter. Exporter prefixes such as `Armature|` are ignored.

| Clip | Plays | What it shows |
| --- | --- | --- |
| `Idle` | loop, 4 to 8 s, seamless | Slight breathing, a small weight shift, small head and shoulder movement. Calm, never distracting. |
| `Welcome` | once, 2 to 3 s | Looks at the viewer, raises one arm and waves using shoulder, elbow, wrist and hand, small head tilt or nod, friendly face. Ends close to the Idle pose. |
| `Thinking` | loop, 3 to 6 s, seamless | Shifts posture, looks up or to the side, hand towards the chin, thoughtful face. |
| `Success` | once, 1.5 to 2.5 s | Thumbs up with a nod and a smile. |
| `Celebrate` | once, 2 to 3.5 s | Bends the knees, pushes up and jumps with both arms up, feet clearly leaving the ground, lands naturally, optionally a partial turn showing the side or back before facing forward again. |
| `Encourage` | once, 1.5 to 2.5 s | A supportive gesture: thumbs up, nod, or a hand pointing towards the student's work. |

Rules for every clip:

- Animate in place. The hips may move up and down (jumps) and turn, but the character must end where it started, facing +Z.
- One-shot clips should start and end near the Idle pose, so the 0.4 s blend in and out looks natural.
- Turns must be real rotations of the body, not a flipped image.

Optional building blocks: `Wave`, `ThumbsUp`, `Yes` (nod), `Jump`, `Turn`. If the file has no `Welcome` clip but has `Wave`, the app uses `Wave`. If it has no `Celebrate` clip but has `Jump` and `Turn`, it plays them one after the other. The full fallback list is in `public/static/js/beral/animations.js`.

## How it works in the app

| Part | File |
| --- | --- |
| States, fallback clips and facial expressions | `public/static/js/beral/animations.js` |
| Character engine (Three.js, GLTFLoader, AnimationMixer, crossfades, blinking, light pulse, pausing, clean up) | `public/static/js/beral/beral3d.js` |
| Placement, speech bubble, app events, picture fallback | `createMascot()` in `public/static/js/app.js` |
| Messages and which animation each one plays, model detection | `mathhelper/mascot.py` |
| Three.js r170, loaders and decoders (MIT licence) | `public/static/vendor/three/` |

Events and the animation they play:

| Event | Animation |
| --- | --- |
| First page of a browsing session | `welcome` |
| A problem is being solved (on the loading card) | `thinking` |
| The tutor is writing an answer | `thinking` |
| A problem is solved, a lesson is completed, the first correct practice answer | `success` |
| A practice round of 80% or more | `celebrate` |
| Practice round below 80%, every third correct answer in a row, a wrong answer, saving a solution | `encourage` |

One-shot animations blend back to `idle` by themselves.

### Where Beral appears

- On wide screens with free space beside the page, Beral stays in that margin and idles quietly between events.
- Otherwise he pops up in the lowest corner that covers no button, input, answer, equation or navigation, and leaves after the animation and message.
- On phones and tablets he is smaller. If there is no free spot, he does not appear.

### When the app uses the picture instead of 3D

- No model is installed.
- The model fails to load, or the browser loses the WebGL context.
- WebGL or import maps are not supported.
- The user asked for reduced motion.
- Data saver is on, or the device reports less than 2 GB of memory.

In each of these cases the four pictures are used with the same messages.

### Performance

- Three.js and the model are downloaded only when a model exists, after the page has loaded.
- Drawing stops while Beral is hidden or the tab is in the background.
- Idle and thinking are drawn at 30 frames per second, other moves at the screen rate.
- Pixel ratio is capped at 1.75 (1.5 on touch devices).
- There are no shadows or post effects, and the scene has three lights.

## Testing

- **Admin preview:** `/admin/beral` plays every state and lists found and missing clips, bones and face shapes.
- **Browser console**, on any student page:
  - `beral.play("celebrate")`, which also works with `idle`, `welcome`, `thinking`, `success` and `encourage`
  - `beral.think(true)` and `beral.think(false)`
  - `beral.say("milestone")` for a message with its animation
  - `beral.mode`, which is `3d` or `picture`
- **Real events:** solve a problem, finish a lesson, play a practice round.
- **Fallbacks:** turn on reduced motion in the operating system, or rename the GLB, and Beral becomes the picture again.

## Adding a new animation later

1. Ask the artist for a new clip in the same GLB, for example `Confused`.
2. Add a state in `animations.js`:

   ```js
   confused: { options: [["Confused"]], expression: "thoughtful" },
   ```

3. Play it with `beral.play("confused")`, or give a message that animation in `MESSAGES` in `mathhelper/mascot.py`.

No other code needs to change.
