# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This recommender suggests songs from a small catalog based on a user's taste profile.
It is built for classroom exploration, not a real app.

The system assumes the user can describe three things about themselves: a favorite genre,
a favorite mood, and a target energy level (low, medium, or high). It does not learn
from listening history or feedback — it scores every song against those three inputs
and returns the top five.

---

## 3. How the Model Works

Every song gets a score out of 4.0. The score is built from three checks:

1. **Genre match** — If the song's genre matches your favorite genre, it gets 1 point.
   If not, it gets 0. This is an all-or-nothing check.

2. **Mood match** — Same idea. If the song's mood matches yours, it gets 1 point.

3. **Energy closeness** — Energy is measured on a scale from 0.0 (very calm) to 1.0
   (very intense). The closer a song's energy is to your target, the more points it
   earns — up to 2 points for a perfect match. This is the only gradual check; the
   other two are yes/no.

The song with the highest total score is recommended first.

One change was made from the original design: energy was given twice as much weight
(up from 1 point max to 2 points max), and genre was cut in half (from 2 points to
1 point). The idea was to see whether energy similarity is a stronger signal than
genre label when predicting what someone wants to hear.

---

## 4. Data

The catalog has 18 songs. Each song has a genre, mood, energy level, tempo, and a
few other audio features like acousticness and danceability.

Genres in the catalog: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop,
r&b, classical, edm, country, metal, folk, reggae — 15 genres total.

Moods in the catalog: happy, chill, intense, relaxed, moody, focused, uplifting,
romantic, melancholic, euphoric, nostalgic, angry, somber, peaceful — 14 moods total.

Lofi is the only genre with 3 songs. Pop has 2. Every other genre has exactly 1.
Chill is the only mood with 3 songs. Happy and intense each have 2. Every other mood
has exactly 1.

Nothing was added or removed from the dataset. Some parts of musical taste are missing
entirely — there is no classical beyond one song, no blues, no soul, and no Latin music.
There are also no songs in the moderate energy range (roughly 0.59 to 0.74), which
creates a gap that hurts users who prefer a middle-ground vibe.

---

## 5. Strengths

The system works well for users whose preferences match the catalog's most common
genres and moods. A lofi fan who wants chill, low-energy music gets a clean and
sensible top three — all lofi, all low energy, all calm.

It also handles clear extremes well. A high-energy EDM fan immediately gets the one
EDM song ranked first, with a near-perfect score. The scoring logic is transparent:
you can read the reason line for each song and understand exactly why it ranked where
it did.

The energy term behaves correctly as a continuous signal. Songs that are slightly off
your target are ranked below songs that are very close, which matches how listening
preferences actually work — a small energy mismatch feels different from a large one.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

**Single-song mood lock-in.** Eleven of the fourteen distinct moods in the catalog appear in exactly one song, which means the mood-matching bonus is effectively wired to a single fixed track for most users. For example, a user whose favorite mood is "romantic" can only ever earn the mood bonus from *Velvet Hours* (r&b); every other song in the catalog scores zero on mood regardless of how emotionally similar it might feel. This creates an invisible ranking ceiling: two users who differ only in their stated mood preference can receive completely different top-five lists, not because the songs suit them differently, but because one mood happens to have three catalog entries while another has only one. The system therefore rewards users whose tastes align with overrepresented moods — in this catalog, "chill" (3 songs) — while quietly penalizing users with rarer preferences, a subtle form of popularity bias dressed up as personalization.

**Energy gap in the catalog.** No songs exist between energy 0.59 and 0.74. Any user
whose target energy lands in that range will always face a penalty on every song. Their
scores will be lower across the board compared to users whose targets sit in the
clusters where songs actually exist.

**Exact genre string matching.** "indie pop" and "pop" are treated as completely
different genres. A pop fan gets zero genre credit for *Rooftop Lights* even though it
is a pop-adjacent song. Subgenres are invisible to the system.

**Four audio features are collected but never used.** Tempo, danceability, valence, and
acousticness are loaded from the CSV and stored in the song data, but the scoring
function never reads them. The user profile also includes a "likes acoustic" field that
the system ignores entirely. A user who says they prefer acoustic music gets the same
recommendations as one who does not.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

**Profiles tested.** Four archetypal users were run against the full 18-song catalog to observe how changes in genre, mood, and energy preference affected the ranked output: (1) a high-energy EDM fan (target energy 0.95, mood "euphoric"), (2) a chill lofi student (target energy 0.40, mood "chill"), (3) a moderate jazz lover (target energy 0.50, mood "relaxed"), and (4) a moderate pop listener (target energy 0.60, mood "happy"). Each profile was chosen to sit in a different region of the energy spectrum and to represent both well-represented and underrepresented catalog niches.

**What I looked for.** The primary check was whether the top results were genre- and mood-coherent — that is, whether a pop fan saw pop songs, not metal. A secondary check was whether the energy term was pulling unexpected songs into the top three, especially after the weight-shift experiment doubled energy's contribution.

**What surprised me.** The jazz lover's second and third results were reggae and country — genres with no stylistic overlap with jazz — because they happened to have the closest energy values (0.51 and 0.55 vs. target 0.50). The genre and mood scores were both zero for these songs; they ranked purely on energy proximity. This showed that once the single matching genre song is accounted for, the rest of the list is effectively sorted by energy alone, with genre and mood becoming irrelevant tiebreakers. A second surprise was that the EDM fan's top-three included metal (*Iron Veil*, energy 0.97) ranked equal to pop (*Gym Hero*, energy 0.93) — two genres with opposite cultural associations receiving identical scores because the scoring function has no concept of sonic or cultural distance, only numerical energy difference.

---

## 8. Future Work

The biggest improvement would be using the four features the system already collects
but ignores. Adding acousticness to the score would help separate a jazz fan from a
synth fan even when their energy targets are the same.

Fuzzy genre matching would help a lot. Right now "indie pop" and "pop" score zero for
genre overlap. A simple fix would be to check whether one genre string contains the
other and award partial credit.

Diversity would also improve the experience. Right now the top five can be all lofi
songs for a lofi fan. A re-ranking step that penalizes repeated genres after the first
result would surface more variety while still keeping the best match at #1.

Longer-term, using listening history to adjust weights per user would make the system
actually personalized rather than just preference-filtered. Right now every user who
says they like lofi gets the same three songs in the same order.

---

## 9. Personal Reflection

**Biggest learning moment.**
The weight-shift experiment. Changing energy from 1 point to 2 points felt minor, but
the jazz lover's #2 and #3 results became reggae and country overnight. A weight is not
just a dial — it decides which dimension the whole system cares about most.

**How AI tools helped, and when I had to double-check.**
AI surfaced the mood dead-zone problem (11 of 14 moods appear in only one song) in a
way I would not have caught just by reading the CSV. But I still had to verify the
boundary math myself to confirm the max score stayed at 4.0 after the weight change.
AI flagged the patterns; I checked the arithmetic.

**What surprised me about simple algorithms feeling like recommendations.**
The lofi profile returned a clean, sensible playlist — calm, low energy, study-friendly.
It felt smart. But it only worked because the catalog happened to cover that taste well.
The jazz profile used identical logic and surfaced reggae and country. Same algorithm,
different data coverage, completely different quality. That gap between "feels smart"
and "is smart" was the most useful thing I learned.

**What I would try next.**
Wire in the `acousticness` field — it is already collected, just never scored. Add a
diversity penalty so the same genre cannot appear more than twice in the top five. Test
fuzzy genre matching so "indie pop" gets partial credit for a "pop" fan instead of zero.