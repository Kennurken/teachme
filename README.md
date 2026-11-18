# Teach Me

Teach Me — конспектті жеке оқу жаттықтырғышына айналдыратын Django жобасы (зертханалық жұмыс №8).
Жол: конспект енгізу → 3–8 сұрақ/жауап карточкасы → SQLite-қа сақтау → бетті ашып, жауаптарды қайталау.

## Орнату

macOS / Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python manage.py migrate
./.venv/bin/python manage.py runserver 127.0.0.1:8000
```

Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Сосын браузерде http://127.0.0.1:8000/ аш.

## Режимдер

- **DEMO** (әдепкі): сабақтағы тұрақты «Компьютерные сети» конспекті мен дайын 3 карточка. AI шақырылмайды, желі қажет емес. DEMO тек дайын мысал мәтінімен жұмыс істейді; басқа мәтінге қате көрсетеді.
- **LIVE** (міндетті емес): Gemini API арқылы карточка жасау. `.env.example` файлын `.env` деп көшіріп, мәндерді толтыр:

```
TEACHME_MODE=live
GEMINI_API_KEY=
GEMINI_MODEL=
GEMINI_TIMEOUT_SECONDS=25
```

`GEMINI_TIMEOUT_SECONDS` 1–60 секунд аралығында болуы керек. LIVE режимі осы жобада нақты кілтпен тексерілмеген.

## Қауіпсіздік және шектеулер

- `.env` ішіндегі кілт — құпия. `.env` пен `db.sqlite3` `.gitignore` арқылы commit-ке кірмейді.
- Авторизация және иесі (owner) жоқ: жергілікті сервердегі кез келген адам барлық конспектті көреді. Бұл тек жергілікті оқу жобасы, `DEBUG=True`.
- `source_quote` тексеруі дәйексөздің конспект мәтінінде дәл бар екенін ғана растайды. Жауаптың дұрыстығын растамайды.
- Бір карточка қате болса, бүкіл жауап қабылданбайды. Сақтау бір `transaction.atomic` ішінде өтеді: қате болса жартылай жазба қалмайды.

## Тексеру

Бұл командаларды студент өзі орындайды:

```bash
./.venv/bin/python manage.py check
./.venv/bin/python manage.py test study
./.venv/bin/python manage.py makemigrations --check --dry-run
```

Жергілікті нәтиже (DEMO режимі): `check` — қатесіз; `test study` — 6 тест, OK; `makemigrations --check --dry-run` — No changes detected.
