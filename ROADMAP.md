# 🗺️ GalaxyWizard Roadmap

This document lays out a multi-phase plan to evolve GalaxyWizard from an
alpha-stage tactical RPG (forked from GalaxyMage, 2006) into a modern,
moddable game with a polished engine, powerful creation tools, and
beautiful visual effects.

Each phase builds on the previous one. Items are grounded in the current
codebase (`src/engine`, `src/gui`, `src/ai`, `src/data`) and reference the
files they affect. Checkboxes track progress; contributions are welcome on
any unchecked item.

---

## Guiding Goals

1. **A better game engine** — modern rendering, clean architecture, stable data formats.
2. **A great map creator** — grow `MapEditorGUI` into a full-featured editor.
3. **A character creator** — visual class/unit designer replacing hand-written Python data files.
4. **A campaign creator** — chain scenarios into full campaigns with story, persistence, and branching.
5. **Beautiful visual effects** — particles, shaders, and animations for magic and combat.
6. **A thriving modding community** — safe, documented, shareable content formats.

---

## How to Read the Estimates 📐

Every phase below includes an **Effort & cost** table. Assumptions:

- **Effort** is in **dev-days**: one focused day of work by a developer already
  familiar with Python; ranges cover best case → realistic case. A hobbyist
  contributing 2 days/week completes ~8 dev-days/month.
- **Complexity** rates technical risk, not size: 🟢 routine, 🟡 needs design
  care, 🔴 hard/risky (unknowns, cross-cutting changes, or specialist skills).
- **Skills** flags where general Python experience is not enough
  (OpenGL/GLSL, netcode, game design, art).
- **Cost (outsourced)** is illustrative only, at a blended freelance rate of
  **€350/dev-day** — useful for comparing phases, or for budgeting if parts
  are ever contracted out. For a volunteer project the real currency is
  contributor time.

Estimates cover implementation + tests + documentation, but **not** the
creation of new art/audio assets (see Open Questions below).

---

## Phase 1 — Engine Foundation 🏗️

*Goal: pay down 2006-era technical debt so every later feature is easier to build.*

### 1.1 Rendering modernization
- [ ] Replace immediate-mode OpenGL (`glBegin`/`glVertex`, ~88 call sites in
      `src/gui/GLUtil.py`) with vertex buffer objects (VBOs) and a small
      renderer abstraction (`Renderer` class owning meshes, textures, draw calls).
- [ ] Introduce a minimal shader pipeline (GLSL): one program for terrain,
      one for sprites/billboards, one for UI. Keep a fixed-function fallback
      flag during the transition.
- [ ] Batch map-tile geometry into a single mesh per chunk instead of
      per-tile draw calls (big win for large maps in `Map.py`/`GLUtil.py`).
- [ ] Texture atlas support so tile/sprite textures bind once per frame.
- [ ] Frustum culling and simple level-of-detail for large battlefields.

### 1.2 Architecture cleanup
- [ ] Decouple `src/engine` from Twisted (`pb.Copyable` is inherited by core
      classes like `Effect`, `Scenario`, `Unit`); move serialization into a
      dedicated `netsupport` adapter layer so the engine runs headless.
- [ ] Extract a proper game loop with fixed-timestep simulation and
      interpolated rendering (currently mixed into `MainWindow`/`ScenarioGUI`).
- [ ] Introduce an event bus (publish/subscribe) so GUI, sound, AI, and
      network observe battle events instead of being called directly from
      `Battle.py`.
- [ ] Split `Sprite.py` (1,095 lines) and `ScenarioGUI.py` (919 lines) into
      focused modules (unit rendering, animations, HUD, menus).
- [ ] Add type hints to `src/engine` and enforce with pyright (already
      configured in `pyproject.toml`).

### 1.3 Safe, stable data formats
- [ ] Replace `exec()`-based Python data files (maps, scenarios, classes,
      abilities in `src/data/`) with a declarative format (YAML or JSON with
      a schema). Python files remain supported for advanced scripting, but
      standard content becomes data, not code.
- [ ] Write converters: existing `src/data/demo/maps/*.py` and
      `scenarios/*.py` auto-migrate to the new format.
- [ ] Versioned save-game format (currently no save/load mid-battle).
- [ ] Document all formats in `doc/file-formats.md` as the single source of truth.

### 1.4 Quality infrastructure
- [ ] Raise test coverage of `src/engine` (Battle, Effect, Range, Map) to a
      meaningful baseline; keep the existing pytest + coverage setup honest.
- [ ] Headless engine tests (no OpenGL context) enabled by 1.2 decoupling.
- [ ] Performance benchmarks: frame time on a 40×40 map with 20 units.

### Effort & cost — Phase 1

| Work package | Effort (dev-days) | Complexity | Skills beyond Python | Cost (outsourced) |
|---|---|---|---|---|
| 1.1 Rendering modernization | 25–35 | 🔴 | OpenGL 3.3+, GLSL, profiling | €8.8k–12.3k |
| 1.2 Architecture cleanup | 15–25 | 🟡 | Refactoring at scale, Twisted | €5.3k–8.8k |
| 1.3 Safe, stable data formats | 10–15 | 🟡 | Schema design | €3.5k–5.3k |
| 1.4 Quality infrastructure | 8–12 | 🟢 | pytest, CI | €2.8k–4.2k |
| **Total** | **58–87** | | | **€20k–30k** |

**Duration:** ~3–4 months for one full-time dev; 8–11 months for a hobbyist
at 2 days/week. 1.3 and 1.4 can run in parallel with 1.1 by a second
contributor.

**Key risks:**
- *Renderer rewrite stalls the project* (🔴): mitigate by migrating one
  draw path at a time behind a `--legacy-gl` fallback flag, keeping the game
  shippable at every commit.
- *PyOpenGL performance ceiling*: if VBO batching still can't hold 60 fps on
  large maps, evaluate `moderngl` as the GL binding before writing more
  renderer code (decision point at end of 1.1 batching work).
- *Hidden Twisted coupling* in `Unit`/`Effect` serialization may make 1.2
  larger than estimated; time-box a 2-day spike first to map the coupling.

**Milestone:** the demo scenarios run identically, but on the new renderer,
with the engine importable without pygame/OpenGL/Twisted.

---

## Phase 2 — Beautiful Visual Effects ✨

*Goal: make magic and combat feel spectacular. Depends on Phase 1's shader
pipeline and event bus.*

### 2.1 Particle system core
- [ ] GPU-friendly particle system (single VBO, point sprites or textured
      quads): emitters, lifetime, velocity/gravity, color-over-life,
      size-over-life, additive blending.
- [ ] Data-driven particle definitions (`src/data/core/effects/*.yaml`) so
      modders can create effects without code.
- [ ] Effect events: the event bus emits `AbilityUsed`, `UnitDamaged`,
      `UnitHealed`, `UnitDied`; the VFX layer maps them to particle effects.

### 2.2 Magic effects by school
Damage types already exist in `src/engine/Effect.py` (FIRE, ICE, HOLY,
HEALING, plus physical types) — give each a signature look:
- [ ] 🔥 **Fire**: ember burst, rising smoke, orange point-light flash,
      scorch decal on the tile.
- [ ] ❄️ **Ice**: crystal shards, frost mist, blue-white glint, brief
      frozen tint on the target sprite.
- [ ] ✨ **Holy**: descending light column, golden sparkles, soft bloom.
- [ ] 💚 **Healing**: rising green motes, gentle pulse ring on the ground.
- [ ] ⚔️ **Physical**: impact sparks, dust puffs on landing, slash arcs.
- [ ] Projectile effects for ranged abilities: arcing missiles with trails
      that travel from caster to target before the impact effect plays.

### 2.3 Combat feedback & juice
- [ ] Floating damage/heal numbers with easing and crit emphasis.
- [ ] Hit flash / knockback nudge on the target sprite.
- [ ] Screen shake (subtle, configurable, off by default in settings).
- [ ] Ability cast telegraphs: highlight affected tiles with animated
      area-of-effect overlays (extends the existing highlight system).
- [ ] Death animations: fade + dissolve instead of instant removal.

### 2.4 World & atmosphere
- [ ] Animated water tiles (scrolling normal/texture offset on `lake.py`-style maps).
- [ ] Weather effects: rain, snow, fog — selectable per scenario via the
      existing `Light`/lighting-environment system (`lighting-*.py` scenarios).
- [ ] Day/night lighting transitions and point lights for fire effects
      (extend `src/engine/Light.py`).
- [ ] Post-processing pass (optional, shader-based): bloom for magic,
      vignette, damage flash.

### Effort & cost — Phase 2

| Work package | Effort (dev-days) | Complexity | Skills beyond Python | Cost (outsourced) |
|---|---|---|---|---|
| 2.1 Particle system core | 10–15 | 🟡 | GLSL, blending/perf | €3.5k–5.3k |
| 2.2 Magic effects by school | 10–15 | 🟡 | VFX design eye | €3.5k–5.3k |
| 2.3 Combat feedback & juice | 6–10 | 🟢 | Animation/easing | €2.1k–3.5k |
| 2.4 World & atmosphere | 10–15 | 🟡 | GLSL (post-processing) | €3.5k–5.3k |
| **Total** | **36–55** | | | **€12.6k–19.3k** |

**Duration:** ~2–2.5 months full-time. Requires 1.1 (shader pipeline) and the
event bus from 1.2; does **not** need 1.3, so it can start before the data
migration finishes.

**Key risks:**
- *Effects need artistic taste, not just code*: the difference between
  "particles" and "beautiful" is iteration time. Budget ~30% of 2.2 for
  tuning; recruit a contributor with VFX/art sensibility if possible.
- *Particle textures/sprites must come from somewhere*: plan on CC0/CC-BY
  packs (e.g. Kenney, OpenGameArt) — flagged in Open Questions.
- *Post-processing (2.4) on old GPUs*: make bloom/vignette strictly optional
  with auto-detection and a settings toggle.

**Milestone:** casting Fireball looks and feels like a fireball — telegraph,
projectile, explosion, numbers, shake — all data-driven.

---

## Phase 3 — Map Creator 🗺️

*Goal: turn the existing in-game editor (`MapEditorGUI.py`,
`MapEditorCursor.py`, `MapEditorSprite.py`) into a tool people enjoy using.*

### 3.1 Editor usability
- [ ] Undo/redo stack for all edit operations.
- [ ] Brush tools: raise/lower/flatten/smooth terrain, single-tile and
      multi-tile brush sizes.
- [ ] Rectangle/lasso selection with copy, paste, mirror, and rotate.
- [ ] Texture painting with a palette panel showing all tile textures
      (`src/data/core/textures`, `src/data/demo/textures`).
- [ ] Live minimap and camera bookmarks.
- [ ] New Map wizard: dimensions, base height, base texture, optional
      procedural seed (reuse `engine/MapGenerator.py`).

### 3.2 Map features
- [ ] Water level, impassable flags, movement-cost per tile — editable in
      the tile inspector (extends the existing tag system / `tileInfoDisplayer`).
- [ ] Prop/doodad placement (trees, rocks, banners) as a new map layer.
- [ ] Spawn zones: paint player/enemy deployment areas directly on the map.
- [ ] Save/load in the new declarative format (Phase 1.3) with backwards
      compatibility for `.py` maps.

### 3.3 Procedural generation upgrades
- [ ] Expand `MapGenerator.py`: biome presets (mountains, swamp, castle,
      ruins), symmetric maps for multiplayer fairness.
- [ ] "Generate → edit" flow: generate a map in the editor, then hand-tune it.

### 3.4 Playtest loop
- [ ] "Test Battle" button: jump from editor into a skirmish on the current
      map with placeholder units, then return to editing.

### Effort & cost — Phase 3

| Work package | Effort (dev-days) | Complexity | Skills beyond Python | Cost (outsourced) |
|---|---|---|---|---|
| 3.1 Editor usability | 12–18 | 🟡 | UX for tools | €4.2k–6.3k |
| 3.2 Map features | 8–12 | 🟢 | — | €2.8k–4.2k |
| 3.3 Procedural generation | 5–8 | 🟡 | Procgen algorithms | €1.8k–2.8k |
| 3.4 Playtest loop | 2–4 | 🟢 | — | €0.7k–1.4k |
| **Total** | **27–42** | | | **€9.5k–14.7k** |

**Duration:** ~1.5–2 months full-time. Only hard dependency is the map file
format from 1.3 (saving in the new format); brush/undo work can start on the
current `.py` format and switch later.

**Key risks:**
- *Undo/redo retrofitted late is painful*: implement the command pattern
  **first** in 3.1 so every subsequent tool is undoable by construction.
- *Editor UI debt*: the current editor uses ad-hoc menus; consider a minimal
  immediate-mode UI helper (or `pygame_gui`) before building panels/palettes,
  otherwise each panel is bespoke OpenGL text layout.

**Milestone:** create, texture, decorate, and playtest a map without
touching a text editor.

---

## Phase 4 — Character Creator 🧙

*Goal: visual creation of classes, units, abilities, and equipment —
currently hand-written Python in `src/data/core/classes`, `abilities`,
`items` and `src/data/demo/units`.*

### 4.1 Class & unit designer
- [ ] In-game class editor: stats, growth curves, movement/jump ranges,
      equippable weapon types — with live stat preview at any level
      (drives `engine/Class.py` / `engine/Unit.py`).
- [ ] Unit designer: name (integrate `engine/Name.py` random generator),
      class, level, faction, starting equipment, sprite selection.
- [ ] Sprite/portrait picker from available image assets, with palette-swap
      recoloring for team colors and variants.
- [ ] Balance dashboard: compare classes side by side (damage per turn,
      effective HP, mobility radar chart).

### 4.2 Ability designer
- [ ] Ability editor: cost, range/area (visual range preview using
      `engine/Range.py` shapes), damage type, power, status effects.
- [ ] Attach VFX (Phase 2) and sounds to abilities from dropdowns.
- [ ] Effect composition UI mirroring `engine/Effect.py` primitives
      (damage, healing, status, push/pull) so new abilities need no code.

### 4.3 Equipment designer
- [ ] Weapon/armor/accessory editor for `engine/Equipment.py` items:
      stat modifiers, damage types, class restrictions.

### 4.4 Progression systems (engine work)
- [ ] Deepen leveling: stat growth per class, class change requirements,
      learned-ability trees.
- [ ] Status effects framework: poison, slow, haste, shield, charm — with
      icons, durations, and VFX hooks.

### Effort & cost — Phase 4

| Work package | Effort (dev-days) | Complexity | Skills beyond Python | Cost (outsourced) |
|---|---|---|---|---|
| 4.1 Class & unit designer | 10–15 | 🟡 | UI, game balance | €3.5k–5.3k |
| 4.2 Ability designer | 8–12 | 🟡 | UI | €2.8k–4.2k |
| 4.3 Equipment designer | 3–5 | 🟢 | — | €1.1k–1.8k |
| 4.4 Progression systems | 8–12 | 🟡 | Game design | €2.8k–4.2k |
| **Total** | **29–44** | | | **€10.2k–15.4k** |

**Duration:** ~1.5–2 months full-time. Hard dependencies: 1.3 (editors write
the declarative format) and 2.2 (assigning VFX to abilities). Reuses the UI
foundation chosen in Phase 3 — building it there first is why Phase 4 comes
after.

**Key risks:**
- *Status effects (4.4) touch everything*: `Battle`, `Unit`, AI, serialization,
  and UI all need to understand them. Design the framework on paper (issue +
  review) before coding; this is the item most likely to overrun.
- *Balance tooling is open-ended*: time-box the balance dashboard; a simple
  side-by-side table delivers 80% of the value.

**Milestone:** build a brand-new class with a custom ability and matching
visual effect entirely in-game, and use it in a skirmish.

---

## Phase 5 — Campaign Creator 📖

*Goal: today the game only runs standalone scenarios chosen from
`ScenarioChooser`. Add full campaigns: sequences of battles with story,
persistent parties, and branching.*

### 5.1 Campaign engine
- [ ] Campaign definition format: ordered nodes (battle, story scene, shop,
      rest), win/lose transitions, optional branching conditions.
- [ ] Persistent party state across battles: roster, XP/levels, equipment,
      inventory, gold — with save/load (builds on Phase 1.3 saves).
- [ ] World map screen: node graph of the campaign with completed/available
      locations.
- [ ] Between-battle screens: party management, equipment shop, unit
      recruitment.

### 5.2 Story & dialogue
- [ ] Dialogue system: portraits, speaker names, text pages, simple choices.
- [ ] In-battle scripted events: dialogue triggers on turn N / unit death /
      tile reached; reinforcement spawns mid-battle.
- [ ] Cutscene primitives: camera pans (extend `gui/Camera.py`), unit
      walk-ons, music changes.
- [ ] Localization of campaign text through the existing `src/locale`
      system (en/fr already present).

### 5.3 Campaign editor
- [ ] Visual node-graph editor: drag battle/story/shop nodes, connect
      victory/defeat edges.
- [ ] Dialogue editor with portrait/speaker preview.
- [ ] Objective editor per battle: defeat all, defeat boss, survive N
      turns, reach tile, protect unit (extends `engine/Battle.py` win
      conditions).
- [ ] One-click campaign packaging (Phase 6 mod format) for sharing.

### 5.4 Flagship content
- [ ] Ship a 10–12 battle official campaign exercising every feature —
      it doubles as the tutorial and the reference example for creators.

### Effort & cost — Phase 5

| Work package | Effort (dev-days) | Complexity | Skills beyond Python | Cost (outsourced) |
|---|---|---|---|---|
| 5.1 Campaign engine | 15–20 | 🟡 | State/save design | €5.3k–7k |
| 5.2 Story & dialogue | 10–15 | 🟡 | — | €3.5k–5.3k |
| 5.3 Campaign editor | 12–18 | 🟡 | Node-graph UI | €4.2k–6.3k |
| 5.4 Flagship campaign content | 15–25 | 🟡 | Writing, game design | €5.3k–8.8k |
| **Total** | **52–78** | | | **€18.2k–27.3k** |

**Duration:** ~2.5–4 months full-time — the largest phase. Hard dependencies:
save system (1.3), scripted battle events extend `Battle.py` (cleaner after
1.2). 5.4 is content, not code: writers and scenario designers can own it in
parallel once 5.1–5.2 land.

**Key risks:**
- *Save-game compatibility*: campaign saves persist across game updates;
  version the format from day one and write migration tests, or early
  adopters lose their campaigns.
- *Scope creep in dialogue/cutscenes*: cap 5.2 at portraits + choices +
  triggers; branching dialogue trees and full cutscene scripting are
  post-roadmap.
- *Flagship campaign needs writing talent*: recruit for narrative early; code
  being done doesn't make the campaign good.

**Milestone:** play a saved, branching, multi-battle campaign with a
persistent party, created entirely with the campaign editor.

---

## Phase 6 — Modding, Multiplayer & Community 🌐

### 6.1 Modding & sharing
- [ ] Mod package format: a zip with maps, units, campaigns, textures,
      sounds, effects + manifest (name, version, dependencies).
- [ ] Mod loader with load-order and conflict detection (extends the
      existing `resources.py` layered data-directory system:
      core → demo/extra → mods).
- [ ] Creator documentation site generated from `doc/` (formats,
      tutorials, example mods).

### 6.2 Multiplayer revival
- [ ] Audit and stabilize the Twisted-based multiplayer
      (`engine/netsupport.py`, `twistedmain.py`) on the post-Phase-1
      architecture.
- [ ] Lobby flow: host/join, map & army selection, ready checks.
- [ ] Deterministic simulation + command-passing to reduce sync bugs;
      reconnection support.
- [ ] Async/hot-seat play as a low-infrastructure alternative.

### 6.3 Audio
- [ ] Positional sound effects tied to the VFX event system (Phase 2.1).
- [ ] Per-ability cast/impact sounds assignable in the ability designer.
- [ ] Music system: per-scenario tracks (already in `Scenario`), crossfade,
      battle/victory/defeat stingers.

### 6.4 AI improvements
- [ ] Difficulty profiles for `src/ai/UnitAI.py` (aggressive, defensive,
      objective-focused).
- [ ] AI understanding of new systems: status effects, terrain cost,
      objectives, ability synergies.
- [ ] AI personality assignable per unit in the character creator.

### 6.5 Accessibility & polish
- [ ] Rebindable controls (extend `gui/Input.py`), gamepad support.
- [ ] UI scale, colorblind-safe faction palettes, reduced-motion mode
      (disables shake/flash from Phase 2.3).
- [ ] In-game settings menu (currently config-file only).

### Effort & cost — Phase 6

| Work package | Effort (dev-days) | Complexity | Skills beyond Python | Cost (outsourced) |
|---|---|---|---|---|
| 6.1 Modding & sharing | 8–12 | 🟡 | Packaging, docs | €2.8k–4.2k |
| 6.2 Multiplayer revival | 15–25 | 🔴 | Netcode, Twisted | €5.3k–8.8k |
| 6.3 Audio | 5–8 | 🟢 | Sound design | €1.8k–2.8k |
| 6.4 AI improvements | 8–12 | 🟡 | Game AI | €2.8k–4.2k |
| 6.5 Accessibility & polish | 6–10 | 🟢 | UX | €2.1k–3.5k |
| **Total** | **42–67** | | | **€14.7k–23.5k** |

**Duration:** ~2–3 months full-time, but 6.1/6.3/6.4/6.5 are independent of
each other and of 6.2 — ideal for parallel contributors.

**Key risks:**
- *Multiplayer (6.2) is the riskiest item on the whole roadmap*: legacy
  Twisted `pb` code, no test coverage, and desync bugs are notoriously hard.
  Start with a 3-day spike to assess whether to fix the existing netcode or
  rebuild on deterministic lockstep; hot-seat play is the cheap fallback that
  still delivers "play with a friend".
- *Mod loading executes third-party content*: with 1.3 done, standard mods
  are pure data (safe); clearly gate/label mods that ship Python scripts.

---

## Suggested Sequence & Priorities

| Order | Phase | Why first |
|-------|-------|-----------|
| 1 | Phase 1 — Engine Foundation | Everything else builds on the renderer, event bus, and data formats. |
| 2 | Phase 2 — Visual Effects | Highest player-visible impact; validates the new renderer and event bus. |
| 3 | Phase 3 — Map Creator | Smallest gap to close (editor exists); unblocks content creators early. |
| 4 | Phase 4 — Character Creator | Needs stable data formats (1.3) and ability/VFX hooks (2.2). |
| 5 | Phase 5 — Campaign Creator | Largest new system; consumes maps, characters, and effects from 2–4. |
| 6 | Phase 6 — Modding & Community | Packages everything above into a shareable ecosystem. |

Within each phase, items are roughly ordered; the first unchecked item is
usually the right next task. Phases can overlap — e.g. VFX work (2) can
start as soon as the shader pipeline (1.1) lands, without waiting for the
data-format migration (1.3).

---

## Total Budget & Timeline Scenarios 💰

### Overall effort

| Phase | Effort (dev-days) | Cost (outsourced, €350/day) |
|---|---|---|
| 1 — Engine Foundation | 58–87 | €20.3k–30.5k |
| 2 — Visual Effects | 36–55 | €12.6k–19.3k |
| 3 — Map Creator | 27–42 | €9.5k–14.7k |
| 4 — Character Creator | 29–44 | €10.2k–15.4k |
| 5 — Campaign Creator | 52–78 | €18.2k–27.3k |
| 6 — Modding & Community | 42–67 | €14.7k–23.5k |
| **Full roadmap** | **244–373** | **€85k–131k** |

### Timeline by team size

| Team | Phase 1+2 (playable payoff) | Full roadmap |
|---|---|---|
| Solo hobbyist (~2 days/week) | 10–15 months | 2.5–4 years |
| One full-time developer | 4–6 months | 12–18 months |
| 2–3 regular contributors | 3–4 months | 8–14 months |

**Practical reading:** for a volunteer project the realistic near-term target
is **Phases 1–3** (~121–184 dev-days) — a modern engine, spectacular magic,
and a great map editor. That alone is a compelling release ("GalaxyWizard
1.0"), and Phases 4–6 can be re-planned afterwards with community input.

### Where estimates are most likely wrong

- 🔴 items (renderer rewrite, multiplayer) carry the widest variance —
  each has a recommended time-boxed spike before committing.
- Content work (5.4 flagship campaign) scales with ambition, not code.
- No art/audio production is budgeted (see below).

---

## Open Questions / Missing Information ❓

Decisions needed before (or during) the phases that depend on them:

1. **Minimum OpenGL version** (Phase 1.1): OpenGL 3.3 core is the sane
   shader baseline, but drops some very old hardware. Decide the support
   floor before writing shaders. *Owner: maintainer. Needed by: start of 1.1.*
2. **GL binding**: stay on PyOpenGL or adopt `moderngl` (cleaner API, faster,
   but a new dependency)? Decision point after the 1.1 batching spike.
3. **Data format choice** (1.3): YAML (human-friendly, needs `pyyaml`) vs
   JSON (stdlib, noisier to hand-edit) vs TOML. Recommendation: YAML for
   authored content, JSON for saves.
4. **UI toolkit for editors** (Phases 3–5): keep bespoke OpenGL UI, adopt
   `pygame_gui`, or embed an immediate-mode UI (e.g. imgui bindings)? This
   choice shapes ~40 dev-days of editor work — decide at the start of Phase 3.
5. **Art & audio pipeline**: who produces particle textures, portraits,
   props, and per-school sound effects? Options: CC0/CC-BY packs (Kenney,
   OpenGameArt), commissioned art (budget separately, roughly €2k–5k for a
   coherent pack), or AI-assisted generation with license review.
6. **Multiplayer scope** (6.2): real-time online, async/PBEM, or hot-seat
   first? Determines whether the 3-day netcode spike targets Twisted repair
   or a rebuild.
7. **Target platforms & distribution**: PyInstaller builds exist for
   Win/Linux/macOS — is itch.io/Steam distribution a goal? Steam adds
   achievements/workshop opportunities but also QA overhead.
8. **Python version window**: currently `>=3.11,<3.13`; widen to 3.13+ as
   dependencies (numpy pin at 1.24.1 is old) allow — a small 1.4 task.
9. **Funding**: if any budget exists (sponsorware, OpenCollective, grants),
   the highest-leverage spends are commissioned art (Q5) and a contracted
   renderer specialist for 1.1.

---

## Contributing

Pick any unchecked item, open an issue to discuss the approach, and send a
PR referencing the roadmap item. Small, focused PRs preferred — see
`README.md` for development setup (Poetry, ruff, pyright, pytest).
