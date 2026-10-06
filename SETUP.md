# Your animated full stack profile

This kit presents Bernstain O. Fangon as a student building across the full stack. Review the skills and project descriptions and adjust anything that does not reflect what you want to show publicly.

## Put it on GitHub

1. Sign in to GitHub and create a **public repository whose name exactly matches your GitHub username**. If it already exists, back up its README and assets before merging this kit.
2. Extract this ZIP. Copy the **contents** of `FullStack_Profile_Kit` into the repository root. Include `.github/workflows/profile.yml`; some file managers hide `.github`. Do not upload the outer folder or ZIP itself.
3. Commit and push the files. `README.md` must be at the repository root.
4. Open the repository's **Actions** tab, select **Refresh profile telemetry**, and click **Run workflow** on the default branch. If Actions is disabled, enable it first.
5. Open your GitHub profile to see the README. Give updated images time to refresh because GitHub caches them.

The workflow automatically uses the repository owner's username. You do not need to paste an API key or personal access token. The default workflow token reads public profile data and commits the generated SVG files in this repository. Branch protection or repository policies can block the automated commit; inspect the Actions log if the card does not update.

## Included design

- A custom SVG hero with an animated request/response flow across frontend, API, and database layers.
- A cohesive navy, cyan, violet, and emerald palette with readable labels.
- A restrained professional introduction, technology table, and project showcase.
- Matching public stats: all public repositories, followers, and total stars on owned public non-fork repositories.
- A language panel counting primary languages of owned public non-fork repositories. It is a repository count, not a percentage of code or proficiency.
- A daily scheduled refresh at 02:23 UTC (10:23 AM Philippines time). Scheduled jobs can be delayed and public repository schedules may stop after inactivity; use Run workflow to refresh manually.

Initial stats display `—` and “Awaiting first update.” No sample numbers are presented as yours. Assets stay available in the repository even if a later API request fails. Animations do not imply real-time data: the numbers are periodic snapshots.

## Customize

- Change `DISPLAY_NAME`, `DISPLAY_ROLE`, and `TAGLINE` near the top of `scripts/build_profile.py`, then run the workflow.
- Edit `README.md` to change skills, project descriptions, or add real project and contact links. Only OptimaSched has a supplied repository link; the other project names intentionally have no guessed links.
- Change palette values in `scripts/build_profile.py` to generate matching assets. Use a short display name or reduce the hero font size for longer names.
- There are no external image-generation services, tracking badges, paid services, or Python package dependencies.

## Run locally (optional)

With Python 3.10 or later, from this kit's root:

```powershell
python scripts/build_profile.py --username YOUR_GITHUB_USERNAME
```

An unauthenticated run uses GitHub's public API allowance. For an offline starter card:

```powershell
python scripts/build_profile.py --starter
```

The generator writes only `assets/fullstack-banner.svg` and `assets/github-stats.svg`. It never edits your GitHub profile settings or publishes anything by itself.

## Platform notes

The design is embedded as SVG images in a README. It does not change GitHub's surrounding page layout. SVG animation support depends on the viewer; the fixed design remains readable when animations are disabled. The SVG includes reduced-motion styling. Confirm appearance on GitHub after uploading; this kit has not been deployed to your account.

## Sources

- Profile README requirements: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme
- GitHub REST repositories: https://docs.github.com/en/rest/repos/repos
- GitHub REST users: https://docs.github.com/en/rest/users/users
- Workflow syntax: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- Scheduled workflow behavior: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
