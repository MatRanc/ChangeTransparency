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

### v0.1.0

- First release. Adds the **Change Transparency (50% / 100%)** right-click menu item
  for bodies, occurrences, and components, placed after Opacity Control.
- Themed (light/dark) cube icon.

## Credits

The opacity-flip logic mirrors the translucency toggle in the VerticalTimeline add-in.

MIT licensed — see [LICENSE-MIT](LICENSE-MIT).
