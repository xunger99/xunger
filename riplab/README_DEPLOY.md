# AI-Enabled Control Engineering Course Website

This is the English static course website for the PKU College of Engineering GLOBEX Summer Program course **AI-Enabled Control Engineering**.

## Course staff

- Instructor: Xun Huang
- Teaching Assistants: Zhixiang Ju and Haozhe Wang

## What is included

- English homepage and navigation pages
- Course schedule for Classes 6--12
- Downloadable course PDFs, lab-report templates, supplementary theory material, and RIP code packages
- Rotary inverted pendulum code packages
- Lab task/report guide page
- Hardware and software resource page

## What is not included

This website intentionally does **not** include an answer-upload or online submission function. If a submission workflow is needed later, connect the course to a separate LMS, GitHub Classroom, Moodle/Canvas, Microsoft Forms, or a university file-collection system.

## Local preview

```bash
cd globex_ai_enabled_control_english_site
python3 -m http.server 8000
open http://localhost:8000
```

## Common edits

- Edit `data/lectures.json` for lecture titles, descriptions, and slide links.
- Add PDFs to `downloads/slides/`.
- Add student-facing RIP code ZIP files to `downloads/code/` and link them from `code.html`.
- Keep stable ZIP filenames so existing website and course-group links continue to work when the source packages are refreshed.
- Edit staff names in `data/course.json`, `staff.html`, and the footer inside each HTML page if needed.

## Deployment

This is a static site. It can be deployed to GitHub Pages, Netlify, Vercel, or a university web server.
