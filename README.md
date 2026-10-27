# Math Homework Helper

A web app that solves math problems from a photo or typed question, explains every step, and helps students learn with lessons and practice.

Built with Python (Flask), SQLite and Google Gemini. The AI key stays on the server and is never sent to the browser.

## Features

- **Solve**: take or upload a photo (or paste one), or type the problem. Every problem on the page gets an answer, the full working line by line, each step's math line with its explanation underneath, and a tip. There is no level to choose: explanations are written so learners of any age and teachers can follow them.
- **Ask the tutor**: a chat under each solution for simpler explanations, checking your own work, or a similar problem to try.
- **Library**: every solution is saved, with search, topic filters and a Saved tab.
- **Learn**: 13 courses and 39 short lessons from elementary arithmetic to college linear algebra. Each lesson has key ideas, a worked example and a common mistake.
- **My curriculum**: pick a country and school level in Settings (your language is chosen separately and never changes it). Each chapter is a textbook style course: sections with definitions, worked examples where every step is explained, guided exercises with hints, independent practice, a summary and a 12 question assessment with new numbers every time, detailed corrections and revision advice. Answers are checked exactly (3,5, 3.50 and 7/2 are the same number, and a form such as "fully simplified" can be required). Progress is saved per student. A lesson tutor answers questions about the lesson in front of the student, and the solver uses the student's level. See `docs/curriculum.md`.
- **Practice**: 23 skills that generate fresh questions every round, with instant feedback, sounds, keyboard shortcuts, scores and a full review.
- **Progress**: day streak, weekly activity, practice accuracy, lessons completed and personal bests.
- **Admin dashboard**: one admin account runs the platform at `/admin`: an overview of activity, users (view, suspend, reactivate, delete), lessons (add, edit, preview, delete, restore) and practice sets (write your own questions, edit, preview, delete, restore). The admin account has no student pages, and every admin page and action is checked on the server.
- **Accounts**: email and password sign up, Google sign in, password reset by email, profile, theme (light, dark or system), password change and account deletion.
- **Beral**: the mascot greets, thinks while a problem is solved, and celebrates or encourages after real events. Today Beral is shown with four pictures. The app is ready for a rigged 3D Beral (Three.js, GLB with animation clips); see `docs/beral-3d.md` for the model brief, where the file goes and how to test it.
- **English and French**: the app follows the browser language, and a globe switch showing both languages sits at the top of every page (in the sidebar on desktop) and in Settings. Screens, lessons, practice questions, AI answers, emails and the legal pages are all translated.
- Works on phones and tablets (compact layout, bottom tab bar, camera button, account menu with log out) and desktops (sidebar).

## Run it on your computer

Open PowerShell in this folder:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python run.py
```

Then open http://localhost:5000 and create an account.

The `.venv` folder already exists in this project, so on this computer you only need the last line.

## Settings (`.env`)

All your existing keys were kept, so you do not need new ones.

| Name | What it does |
| --- | --- |
| `GEMINI_API_KEY` | Your Google Gemini key. Already filled in. |
| `GEMINI_MODEL` | Main model, `gemini-flash-latest`. |
| `GEMINI_FALLBACK_MODEL` | Used automatically when the main model is busy, `gemini-flash-lite-latest`. |
| `SECRET_KEY` | Signs login sessions. Already generated. Keep it private. |
| `DATABASE_URL` | Leave empty for a local SQLite file in `instance/`. Set a Postgres URL to use a hosted database. |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | Google sign in. The Google button appears once both are set. |
| `SMTP_USER`, `SMTP_PASSWORD` | A Gmail address and its app password. When both are set, password reset emails are sent through Gmail and reach everyone. |
| `RESEND_API_KEY` | Backup sender, used only when the Gmail settings are empty. |
| `MAIL_FROM` | Sender address. Leave empty to use `onboarding@resend.dev`, which can only email the owner of the Resend account. Set it to an address on a domain you verified in Resend to email everyone. |
| `ADMIN_EMAIL`, `ADMIN_PASSWORD` | The one admin account, created when the app starts (password of at least 8 characters). Changing `ADMIN_PASSWORD` resets the admin password at the next start. The live site reads these from Vercel, so copy a new value there and redeploy. A password changed in Settings is kept until `ADMIN_PASSWORD` changes again. |
| `SUPABASE_URL`, `SUPABASE_ANON_KEY` | Kept from the old app. That Supabase project no longer exists, so they are not used. |

Optional extras: `APP_NAME`, `PORT`, `SOLVES_PER_HOUR` (default 30), `QUESTIONS_PER_HOUR` (default 60), `RESET_EMAILS_PER_HOUR` (default 3), `LOGIN_ATTEMPTS` (default 5 wrong passwords) and `LOGIN_WINDOW_MINUTES` (default 15), `SECURE_COOKIES=1` when served over HTTPS, and `BEHIND_PROXY=1` when running behind a proxy. On Vercel the last two turn on by themselves.

### Turning on Google sign in

1. Go to https://console.cloud.google.com/apis/credentials and create an OAuth client ID of type Web application.
2. Add `http://localhost:5000/login/google/callback` as an authorized redirect URI, plus your live address later.
3. Put the client ID and secret into `.env` and restart the app.

## Admin

Log in on the normal login page with `ADMIN_EMAIL` and `ADMIN_PASSWORD` from `.env`. The admin goes straight to the dashboard and only sees Overview, Users, Lessons and Practice. Student pages send the admin back to the dashboard.

- **Overview**: number of users, suspended accounts, lessons and practice sets, plus problems solved, practice rounds and lessons finished this week.
- **Users**: search, see join date and activity, suspend, reactivate or delete. A suspended user is signed out and cannot log in until reactivated.
- **Lessons**: add lessons to any course, edit, preview or delete any lesson, and keep drafts hidden. The built in lessons can always be restored.
- **Practice**: write new practice sets with your own multiple choice questions (2 to 4 choices, optional explanation and French text), or rename and hide the built in sets, which make new questions every round. Built in sets can always be restored.

Deleting always asks for confirmation first. Only the account in `ADMIN_EMAIL` is an admin, and regular users get a "You cannot open this page" error on every admin address.

## Curriculum content and translations

Only reviewed chapters are offered. Today there are nine chapters for Senegal Sixième (decimal numbers, multiplication, division, order of operations, proportionality, fractions, relative numbers, natural numbers and divisibility, statistics). Chapters 5 to 9 are also offered in Côte d'Ivoire, because their lists of contents were compared with the Côte d'Ivoire Sixième programme. Other countries and levels are shown as not yet available. Every chapter says that it has not been checked against the official Senegalese programme.

Lesson text is written once, in French, and translated into English on demand with the Gemini key. Math is set aside before translating and put back unchanged, and a translation that damages a formula is rejected. Translations are stored; the admin can read, correct and delete them in **Admin → Translations**, and a corrected translation is never overwritten. To translate everything ahead of time, so the first student does not wait, run `flask --app wsgi warm-translations` with the production settings.

## Tests

```powershell
.venv\Scripts\python -m pytest
```

The tests use a fake AI, so they run offline and cost nothing.

## Hosting on Vercel

Live at https://math-ai-helper.vercel.app

The app is set up for Vercel: `wsgi.py` is the entry point, `vercel.json` sets the Frankfurt region and a 120 second limit for AI requests, and files in `public/` are served by Vercel's CDN. The Inter font and the KaTeX math library are stored in `public/static/` too, so pages do not depend on outside servers.

Vercel has no permanent disk, so the hosted app needs a Postgres database. Photos are stored in the database for the same reason, and the browser shrinks each photo before upload to stay under Vercel's 4.5 MB request limit.

1. Add a database: in the Vercel project open Storage, create a Neon Postgres database and connect it. This sets `DATABASE_URL` for you. Any other Postgres connection string also works.
2. Add the settings from `.env` under Settings, Environment Variables. Use a different `SECRET_KEY` from the local one.
3. Deploy with `vercel deploy --prod`.
4. In the Google console add `https://YOUR-DOMAIN/login/google/callback` as an authorized redirect URI.

To run a production style server on your own machine instead, use `python run.py --prod`.

## Project layout

```
run.py                 Starts the app on your computer
wsgi.py                Entry point for Vercel and other hosts
vercel.json            Vercel region and time limit
public/static/         CSS, JavaScript and icon
mathhelper/
  __init__.py          App factory, template helpers and error pages
  config.py            Settings from .env
  models.py            Users, solutions, photos, chat messages, practice rounds, lesson progress
  ai.py                Gemini solver and tutor with model fallback
  images.py            Photo checks, resizing and storage
  mailer.py            Gmail or Resend email and password reset links
  schema.py            Database upgrades and the admin account, applied at startup
  accounts.py          Deleting a user's data, shared by Settings and the admin
  mascot.py            Mascot name (Beral), messages and the events that trigger them
  text.py              Safe Markdown with LaTeX math
  stats.py             Streaks and progress numbers
  timeutil.py          Local time zones and friendly dates
  i18n.py              Language choice, translation lookups and localized dates
  translations/fr.py   French text for the interface
  content/             Course and lesson content in English and French
  curriculum/          Country and level catalog, chapters (chapters/), exact answer checker, translation cache, progress, AI context
  practice/            Question generators, and catalog.py for the admin's practice sets
  views/               Routes for each section
  templates/           HTML pages and email templates
tests/                 Automated tests
```
