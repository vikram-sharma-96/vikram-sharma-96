# Publish your profile

These files are prepared for `vikram-sharma-96/vikram-sharma-96` on its `main` branch. They have not been published.

1. Sign in to GitHub as **vikram-sharma-96** and open your existing profile repository.
2. Download and extract the ZIP. Upload the **contents** of the `vikram-sharma-96` folder to the repository root, replacing the starter README. Include `scripts`, `data`, and `.github/workflows/update-profile.yml`. Do not upload only the ZIP or nest everything in another folder.
3. Commit to `main`. The workflow runs after this commit. In **Actions → Refresh contribution artwork**, you can also select **Run workflow**.
4. Visit your GitHub profile to see the result. The graph refreshes around 11:47 AM India time daily; GitHub may delay scheduled runs and cache images.

GitHub Desktop is another option: clone your existing profile repository, copy these files into it (including `.github`), commit, then push. If browser upload omits the dot-folder, create `.github/workflows/update-profile.yml` using **Add file → Create new file** and paste the supplied workflow.

## Personalize

The first version uses your current public avatar and an inferred title, “Learning web development.” Edit `profile.json` for your title, stack, or project. Regenerate the info card with `python scripts/build_profile.py`. Update the README alt text if you change the title.

To convert a new photo into ASCII, install Pillow locally (`python -m pip install Pillow`) and run `python scripts/build_profile.py --avatar path/to/photo.png`. Use a square image with a light, simple background. The daily workflow does not need Pillow, your photo, a personal access token, or any third-party statistics service.

Only generated SVGs, the script, configuration, README, data, and workflow are required. `preview.html` and this setup guide are optional. The calendar comes from GitHub's public contributions HTML; if its markup changes, the script deliberately fails and preserves the last successful artwork rather than inventing activity.
