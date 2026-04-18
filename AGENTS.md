# Agent instructions

## Source of truth for edits

**Apply all code changes in this repository (`Dawn-of-Civilization`).** That includes Python under `Assets/Python`, the CvGameCoreDLL sources that build `Assets/CvGameCoreDLL.dll`, XML, PrivateMaps, and other mod assets tracked here.

## Reference-only paths

Other trees under the parent workspace may exist for playtesting or comparison. **Do not treat them as patch targets** unless the user explicitly asks you to.

Common trap: the installed Civ4 BTS mod folder under:

- `Sid Meier's Civilization IV Beyond the Sword/Beyond the Sword/Mods/RFC Dawn of Civilization`

…is a *playtest/installed* tree (and in this workspace it may even be **vanilla RFC / an external copy**). Treat it as **read-only reference**. Any edits there are easy to lose and won’t be reflected in the repo.

Prefer implementing fixes in this repo, then syncing/building into the playtest folder as needed.

## Docs and tickets

Issue write-ups under `docs/` in the broader RFC Modding folder may link to `Dawn-of-Civilization` paths; when fixing a ticket, match those paths to this repo’s layout.

## Building and Testing

After editing DoC, run **scripts/Sync-DawnModToPlaytest.ps1** from the repo root (PowerShell) to copy `Dawn-of-Civilization` into `Sid Meier's Civilization IV Beyond the Sword\Beyond the Sword\Mods\Dawn-of-Civilization MP`. If you changed **[Dawn-of-Civilization/CvGameCoreDLL](Dawn-of-Civilization/CvGameCoreDLL/)**, run **scripts/Build-CvGameCoreDLL.ps1** first (or **scripts/Deploy-LocalPlaytest.ps1** to build and sync). Follow **docs/reference/playtesting.md** for the standard repro (Babylon + Egypt, RFC 3000 B.C., two `Civ4BeyondSword.exe` clients).