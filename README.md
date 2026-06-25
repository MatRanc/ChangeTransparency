# Change Transparency

A Fusion 360 add-in that brings SolidWorks' **Change Transparency** to Fusion's
right-click menu. Adds a **Change Transparency (50% / 100%)** item that flips the
selected body/component between 50% and 100% opacity — no more digging through the
native Opacity Control submenu.

![context menu](docs/screenshot.png)

## Behavior

- Works on a selected **body**, **occurrence**, or **component** (occurrences have
  no settable opacity, so the component's bodies are flipped), and on multi-selections.
- Toggle rule: if anything in the selection is already transparent, everything goes
  back to 100% opaque; otherwise everything drops to 50%.
- The menu item only appears when the selection has something flippable, and is
  placed right after the native Opacity Control item.

## Install

Self-contained — no dependencies. Download the latest
[release](https://github.com/MatRanc/ChangeTransparency/releases) zip and unzip the
`ChangeTransparency` folder into your Fusion AddIns directory:

- **macOS:** `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
- **Windows:** `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`

(For development you can symlink the repo instead:
`ln -s "$PWD" "$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/ChangeTransparency"`.)

Then in Fusion: **Utilities → Add-Ins** (or `Shift+S`) → select **ChangeTransparency**
→ **Run**. With `runOnStartup` enabled (the default in the manifest) it loads
automatically on launch.

## Tip

Assign a keyboard shortcut to the command via Fusion's UI customization to change
transparency on the selected body with a single keypress.

## Changelog

### v0.1.2

- Fix a crash when right-clicking a **suppressed** occurrence (e.g. a suppressed
  "body to component" feature) — its invalid proxy path threw an
  `InternalValidationError` while building the menu. Suppressed/invalid
  occurrences are now skipped instead.

### v0.1.1

- Fix the menu item vanishing on assemblies / sub-components — `_target_bodies`
  now recurses through child occurrences instead of only flipping a component's
  own bodies.
- Right-clicking a face or edge in the 3D viewport now resolves to its owning
  body, so the toggle works on those picks too.
- Re-running the add-in without a Stop no longer stacks duplicate handlers (which
  duplicated the menu item and flipped twice); the marking-menu insert is also
  idempotent.

### v0.1.0

- First release. Adds the **Change Transparency (50% / 100%)** right-click menu item
  for bodies, occurrences, and components, placed after Opacity Control.
- Themed (light/dark) cube icon.

MIT licensed — see [LICENSE-MIT](LICENSE-MIT).
