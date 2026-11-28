# Novara — Private Search Engine

Novara (formerly PrivaSearch) is a search engine that runs entirely on your own machine. It indexes only
the documents you put in `documents/` — no account, no API key, no cloud
service, and no data leaving the machine.

## What it does

- **Indexer** (`search_engine.py`): tokenises documents, builds an
  inverted index (`term → {doc: term frequency}`), and computes IDF.
- **Ranking**: TF-IDF scoring, with a 1.5× boost for title matches.
  Repeated words use log TF so they can't dominate a result.
- **Snippets**: each result shows a window of text around the first
  matching term.
- **Web UI** (`app.py`): standard-library only, no dependencies.
  Search from a browser, or run `python3 search_engine.py <query>` on
  the command line.

## Run it

```bash
python3 app.py
# open http://127.0.0.1:8000
```

## Website version (GitHub Pages)

The site is branded **Novara**, with a centered logo header, an Inter typeface, a blue-violet gradient Search button, glass cards, tabs (All, Images, Videos, News, Maps, Shopping, Books), an animated placeholder, and the tagline “Search the web, privately. No history, no account, no tracking.”

GitHub Pages can only serve static files, so it cannot run the Python
app above. `index.html` is a static, client-side version of the same
search engine: the same documents, the same tokenising, inverted index,
TF-IDF ranking, title boost, and snippets with your search words
highlighted — all in JavaScript, all in
the browser — plus a clean dark UI and, for any query, a “Results from
the internet” list (up to 12 Wikipedia articles from its free search API, plus
related pages from DuckDuckGo when it has any), a web card from
Wikipedia for a person or topic, many photos in-page (up to 24 from
Wikimedia Commons plus up to 12 from Internet Archive, plus up to 12
from Openverse's free no-key API), and
videos played right in the page from many free sites — up to 4 each
from Wikimedia Commons, Internet Archive, Dailymotion, and PeerTube,
with video embeds lazy-loaded so a search stays fast, search
suggestions as you type (up to 8 topics from Wikipedia's free
opensearch API, no key, picked with ↑ ↓ and Enter, never stored),
a keyboard shortcut: press `/` anywhere to jump to the search box, a
“Clear” button that empties the search box and every result section and
removes the shareable link from the address bar in one tap (in-memory
only, nothing stored), instant answers: type a calculation like
“12 * 8”, “15% of 200”, “what percent of 200 is 25”, “20% off 500”,
“percent increase from 100 to 120” or “sqrt(16)”, or a conversion like “10 km in
miles”, “100 c in f”, “5 acres in sqm”, “2 gb in mb”, “convert 5 km to
miles”, “how many miles is 5 km”, “60 mph in knots” or “10 ft/s in mph”
(length, mass, volume, time, speed including knots and feet per second,
area and file size), and the answer appears at the top, computed
entirely in your browser with a safe parser (never `eval()`), no API
call and nothing stored, weather: type “weather in Mumbai”, “weather
Tokyo” or “Mumbai weather” and the current conditions plus a 3-day
forecast appear at the top, from Open-Meteo’s free no-key API, nothing
stored, air quality: type “air quality in Mumbai”, “AQI in Delhi”,
“pollution in Pune” or “Mumbai air quality” and the current US AQI with
its health category, plus PM2.5 and PM10, appear at the top, from
Open-Meteo’s free no-key Air Quality API, nothing stored, sunrise &
sunset: type “sunrise in Mumbai”, “sunset in Delhi”, “sunrise sunset in
Pune” or “Mumbai sunrise” and today’s sunrise, sunset and day length
appear at the top, from Open-Meteo’s free no-key API, nothing stored,
moon phase: type “moon phase”, “moon tonight”, “full moon” or “when is
the next full moon” and tonight’s moon phase, how lit it is and its
age in days, plus the next full and new moon dates appear at the top,
computed entirely in your browser with no API call and nothing stored,
random: type “roll a dice”, “roll 2 dice”, “roll a d20”, “flip a coin”
or “random number between 1 and 100” and a fresh random result appears
at the top, with a Roll again button to re-roll in place, computed
entirely in your browser with no API call and nothing stored,
password generator: type “generate password”, “random password”,
“create a strong password” or “generate password 16” and a fresh
strong password (8–64 characters, your choice) appears at the top,
with a Copy button and a Generate another button, generated entirely
in your browser with crypto.getRandomValues, no API call and nothing
stored,
dictionary: type “define serendipity”, “meaning of ephemeral”
or “what does ubiquitous mean” and the word, its pronunciation (with
audio), definitions with examples and synonyms appear at the top, from
the Free Dictionary API (free, no key, Wiktionary data), nothing
stored, time: type “time in Tokyo”, “what time is it in London” or
“New York time” and the current time, date and weekday in that city
appear at the top, with your own local time for comparison, computed
entirely in your browser with no API call and nothing stored,
currency: type “100 USD to INR”, “50 dollars in rupees” or “USD to
INR” and the converted amount appears at the top, from
exchangerate-api.com’s free no-key API (160+ currencies, rates
updated daily), nothing stored, countdown: type “days until Christmas”,
“days until 1 January 2027”, “days since 15 August 2026” or “today's
date” and the number of days (or today's date and weekday) appears at
the top, computed entirely in your browser with no API call and nothing
stored, weekday & days between: type “what day of the week is 25
December 2026”, “what day was 15 August 1947”, “what day did 1 January
fall on” or “days between 1 January 2026 and 26 November 2026” and the
weekday of that date, or the number of days between two dates, appears
at the top, computed entirely in your browser with no API call and
nothing stored, translate: type “translate hello to Hindi”, “translate good
morning into Marathi” or “how do you say thank you in Spanish” and the
translation appears at the top, from MyMemory’s free no-key API
(English to Hindi, Marathi, Spanish, French, German, Japanese and 20+
more languages), nothing stored, timer & stopwatch: type “timer 5
minutes”, “set a timer for 10 minutes”, “countdown 90 seconds”, “1 hour
30 minutes timer” or “stopwatch” and a live countdown (with Start/Pause
and Reset buttons, and a beep when time is up) or a count-up stopwatch
appears at the top, computed entirely in your browser with no API call
and nothing stored, age calculator: type “age born 15 August 2000”,
“how old am I if born 1 January 2000” or “my age if I was born 12 March
2001” and your age in years, months and days, plus total days lived and
days until your next birthday, appears at the top, computed entirely in
your browser with no API call and nothing stored, BMI calculator: type
“bmi 70 kg 175 cm” (or “bmi 154 lb 5 ft 9 in”) and your body mass index
with its category (Underweight / Healthy weight / Overweight / Obese)
and the healthy weight range for your height appears at the top,
computed entirely in your browser with no API call and nothing stored,
tip calculator & bill split: type “tip 15% on 800”, “15% tip on 800”,
“tip on 800” (15% by default) or “split 1200 among 4”, “split 1200
between 4 people”, “split 1200 4 ways” or “split 1200 among 4 with 15%
tip” and the tip, the total and what each person pays appear at the
top, computed entirely in your browser with no API call and nothing
stored, EMI calculator: type “emi 500000 10% 5 years”, “loan emi
500000 at 10% for 5 years” or “emi 500000 10 percent 60 months” and
the monthly EMI, total interest and total payable appear at the
top, with a Copy button for the result, computed entirely in your
browser with no API call and nothing stored, GST calculator: type
“gst on 1000 at 18%”, “1000 + 18% gst”, “gst 18% on 1000” or “1180
including 18% gst” and the GST amount, the total with GST and the
CGST/SGST split appear at the top — for an inclusive price the base
price and the GST inside it are worked back out — computed entirely
in your browser with no API call and nothing stored,
and shareable
search links: searching updates the address bar to `?q=your query`
(in place, with no extra history entry and nothing stored), with a
“Copy search link” button, so a pasted link opens the same search.
For the complete, Google-style result set, every search also has
one-tap “see all photos” links (Google Images, Bing Images,
DuckDuckGo Images, Brave Images, Yandex Images, Openverse, Pexels,
Pixabay), “see all videos” links (YouTube, Vimeo, Google Videos,
Bing Videos, DuckDuckGo Videos, Brave Videos, Archive.org,
Dailymotion, PeerTube), and whole-web links to Google, Bing,
DuckDuckGo, Brave, Yahoo, Yandex, Ecosia, Startpage, Qwant and
Mojeek — because full Google/Bing results need a paid API key and a
billion-page index that this free static site does not have, so the
complete “all results” pages live on those search engines and this
site links straight to them for the same query. Web info
uses free public APIs with no account and no key; local documents are
still searched entirely in your browser.

## Privacy: no history

This search engine stores no search history and no watch history:
no cookies, no localStorage, no saved list, no account. The page
itself records nothing you search or play. When you play a video,
that video site itself will see that play, just like visiting it
directly — this page does not record it.

To publish it: in the repo, go to Settings → Pages → Build and
deployment → Deploy from a branch, choose `main` and `/ (root)`, and
save. The site will then be at
`https://tanmaymaind.github.io/private-search-engine-by-Tanmay-Maind-/`

Add your own documents: drop `.txt` or `.md` files into `documents/`
(first line = title) and restart the app. The index rebuilds on startup.

## Tests

```bash
python3 -m pytest tests/ -q
# or, without pytest:
python3 -c "
from search_engine import build_engine
print(build_engine().search('redis cache'))
"
```

## Why this is a good resume project

It is not a CRUD wrapper around someone else's API. You can explain, in
an interview, the data structure (inverted index), the ranking math
(TF-IDF), the trade-offs (title boost, log TF, stopwords), and the
privacy property (local-only by construction) — and then demo it live.
