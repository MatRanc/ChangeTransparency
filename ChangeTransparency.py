# Author-Mathieu
# Description-Change the transparency of selected bodies: toggle between 50% and 100% opacity from the right-click menu.

# =============================================================================
# ChangeTransparency
#
# A Fusion 360 alternative to SolidWorks' "Change Transparency". Adds a
# "Change Transparency (50% / 100%)" item to Fusion's native right-click
# (marking) menu. Click it to flip the selected body/component between 50% and
# 100% opacity, instead of digging through the Opacity Control submenu.
#
# Self-contained: no external libraries. The opacity flip mirrors the one in
# Thomas Axelsson's VerticalTimeline add-in.
#
# Copyright (c) 2026 Mathieu. MIT licensed - see LICENSE-MIT.
# =============================================================================

import adsk.core
import adsk.fusion
import traceback

NAME = 'Change Transparency'
ID_PREFIX = 'matranc_changeTransparency_'
CMD_ID = ID_PREFIX + 'cmd'

TRANSLUCENT = 0.5
OPAQUE = 1.0

app: adsk.core.Application = None
ui: adsk.core.UserInterface = None

# (event, handler) pairs, kept alive so Fusion doesn't garbage-collect the
# handlers, and so stop() can detach them.
_handlers = []

# Entities under the cursor, captured when the marking menu is built and read
# back when the command executes (the menu args are gone by execute time).
_pending = []


def _add_handler(event, handler_cls, callback):
    '''Register `callback` for `event`, wrapped so exceptions surface as a
    message box (Fusion silently swallows them otherwise).'''
    class _Handler(handler_cls):
        def notify(self, args):
            try:
                callback(args)
            except Exception:
                if ui:
                    ui.messageBox(NAME + ' error:\n' + traceback.format_exc())
    handler = _Handler()
    event.add(handler)
    _handlers.append((event, handler))


# =============================================================================
# Lifecycle
# =============================================================================

def run(context):
    global app, ui
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        _remove_ui()  # clean up if a previous stop() did not run

        cmd_def = ui.commandDefinitions.addButtonDefinition(
            CMD_ID,
            'Change Transparency (50% / 100%)',
            'Toggle the selected body/component between 50% and 100% opacity.',
            '')  # no icon: context-menu items render fine without one
        _add_handler(cmd_def.commandCreated,
                     adsk.core.CommandCreatedEventHandler, on_command_created)

        # Inject the command into the native right-click (marking) menu.
        _add_handler(ui.markingMenuDisplaying,
                     adsk.core.MarkingMenuDisplayingEventHandler, on_marking_menu)

        print(NAME + ' running')
    except Exception:
        if ui:
            ui.messageBox(NAME + ' failed to start:\n' + traceback.format_exc())


def stop(context):
    try:
        for event, handler in _handlers:
            event.remove(handler)
        _handlers.clear()
        _remove_ui()
        print(NAME + ' stopped')
    except Exception:
        if ui:
            ui.messageBox(NAME + ' error on stop:\n' + traceback.format_exc())


def _remove_ui():
    cmd_def = ui.commandDefinitions.itemById(CMD_ID)
    if cmd_def:
        cmd_def.deleteMe()


# =============================================================================
# Marking menu + command flow
# =============================================================================

def on_marking_menu(args: adsk.core.MarkingMenuDisplayingEventArgs):
    '''Add our command to the linear (right-click) menu when the selection has
    something whose opacity we can flip.'''
    global _pending
    _pending = [e for e in args.selectedEntities]
    if not any(_target_bodies(e) for e in _pending):
        return

    cmd_def = ui.commandDefinitions.itemById(CMD_ID)
    if not cmd_def:
        return

    controls = args.linearMarkingMenu.controls
    # Place right after the native "Opacity Control" item if we can find it,
    # otherwise just append.
    opacity_id = next((c.id for c in controls
                       if 'opacity' in (c.id or '').lower()), None)
    if opacity_id:
        controls.addCommand(cmd_def, opacity_id, False)  # False = after
    else:
        controls.addCommand(cmd_def)


def on_command_created(args: adsk.core.CommandCreatedEventArgs):
    _add_handler(args.command.execute, adsk.core.CommandEventHandler, on_execute)


def on_execute(args: adsk.core.CommandEventArgs):
    bodies = []
    for entity in _pending:
        bodies += _target_bodies(entity)
    if not bodies:
        return

    # Flip: if anything is already translucent, restore all to opaque;
    # otherwise make them all 50% translucent. (Same rule as VerticalTimeline.)
    try:
        make_opaque = any(b.opacity < 0.99 for b in bodies)
    except (RuntimeError, AttributeError):
        make_opaque = False
    new_opacity = OPAQUE if make_opaque else TRANSLUCENT
    for b in bodies:
        try:
            b.opacity = new_opacity
        except (RuntimeError, AttributeError):
            pass


def _target_bodies(entity):
    '''Bodies whose opacity we flip. Occurrences have no settable opacity, so
    fall through to their component's bodies.'''
    if isinstance(entity, adsk.fusion.BRepBody):
        return [entity]
    if isinstance(entity, adsk.fusion.Occurrence):
        return list(entity.component.bRepBodies)
    bodies = getattr(entity, 'bodies', None)
    if bodies and bodies.count:
        return list(bodies)
    parent = getattr(entity, 'parentComponent', None)
    if parent:
        return list(parent.bRepBodies)
    return []
