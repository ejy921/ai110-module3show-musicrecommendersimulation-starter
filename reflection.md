# Profile Comparison Reflections

These notes compare pairs of the four archetypal user profiles tested against the
18-song catalog. Each comparison focuses on what concretely changed between the two
outputs and why the scoring logic produces that difference.

---

## Pair 1: High-energy EDM fan vs. Chill lofi student

**EDM fan** — `favorite_genre: edm`, `favorite_mood: euphoric`, `target_energy: 0.95`
Top 3: Hyperdrive (edm, 3.98) · Gym Hero (pop, 1.96) · Iron Veil (metal, 1.96)

**Lofi student** — `favorite_genre: lofi`, `favorite_mood: chill`, `target_energy: 0.40`
Top 3: Midnight Coding (lofi, 3.96) · Library Rain (lofi, 3.90) · Focus Flow (lofi, 3.00)

**What changed and why it makes sense.**
These two profiles sit at opposite ends of the energy axis (0.95 vs. 0.40), so they
pull from completely non-overlapping parts of the catalog — high-tempo electronic and
rock songs for the EDM fan, low-tempo bedroom and study music for the lofi student.
This is the expected and correct behavior: energy is the strongest continuous signal,
and both genres happen to cluster tightly in their respective energy ranges in this
catalog, so genre match and energy match reinforce each other.

The notable difference is in *spread*: the lofi student's top three are all lofi songs
(genre lock-in from 3 lofi entries), while the EDM fan's #2 and #3 are pop and metal
— genres with nothing in common with EDM — because the catalog has only one EDM song.
This reveals that the lofi student is in a filter bubble driven by catalog
overrepresentation, while the EDM fan is in a different kind of bubble driven by
catalog underrepresentation. Both are bubbles; the mechanism is opposite.

---

## Pair 2: High-energy EDM fan vs. Moderate jazz lover

**EDM fan** — `target_energy: 0.95`
Top 3: Hyperdrive (edm) · Gym Hero (pop) · Iron Veil (metal)

**Jazz lover** — `favorite_genre: jazz`, `favorite_mood: relaxed`, `target_energy: 0.50`
Top 3: Coffee Shop Stories (jazz, 3.74) · Sun on Water (reggae, 1.98) · Dirt Road Letters (country, 1.90)

**What changed and why it makes sense.**
The jazz lover's top result makes intuitive sense — the one jazz song in the catalog
scores a clean genre + mood + near-energy match. But positions #2 and #3 are reggae
and country, which share no stylistic DNA with jazz. They rank purely because their
energy values (0.51 and 0.55) happen to sit closest to the target of 0.50. The mood
and genre scores are both zero for these songs.

Compared to the EDM fan, the jazz lover's non-#1 results are actually *more*
surprising because the catalog's moderate-energy songs (0.50–0.58 range) are reggae,
country, and r&b — genres that feel farther from jazz than, say, metal feels from
EDM in terms of energy culture. The EDM fan's cross-genre contamination (pop, metal)
at least involves other high-intensity genres. The jazz lover's contamination crosses
into laid-back Americana, which exposes that the system has no concept of genre
family or cultural proximity — only numbers.

---

## Pair 3: Chill lofi student vs. Moderate pop listener

**Lofi student** — `target_energy: 0.40`, `favorite_mood: chill`
Top 3: Midnight Coding (lofi) · Library Rain (lofi) · Focus Flow (lofi)

**Pop listener** — `favorite_genre: pop`, `favorite_mood: happy`, `target_energy: 0.60`
Top 3: Sunrise City (pop, 3.56) · Rooftop Lights (indie pop, 2.68) · Gym Hero (pop, 2.34)

**What changed and why it makes sense.**
Both users have a fairly coherent top-three by feel — the lofi student gets quiet study
music, the pop listener gets upbeat pop songs. But the mechanisms differ in an
instructive way.

The lofi student's list is coherent because of *catalog density*: three lofi songs exist,
and two also match the "chill" mood, so genre + mood + energy all align simultaneously.

The pop listener's list is coherent for a different reason: the catalog's energy dead
zone (0.59–0.74) means the pop listener's target of 0.60 is actually somewhat
misaligned with both pop songs (0.82 and 0.93), yet they still rank #1 and #3 because
genre + mood bonuses compensate. The surprise here is *Rooftop Lights* (indie pop) at
#2: it earns no genre credit because "indie pop" != "pop" (exact-match rule), but it
climbs to second place on mood + energy alone. This is the genre substring trap in
action — the system treats a stylistically close subgenre as completely foreign, yet
the song still surfaces because its other scores are strong enough.

---

## Pair 4: Moderate jazz lover vs. Moderate pop listener

**Jazz lover** — `target_energy: 0.50`, one genre match available
**Pop listener** — `target_energy: 0.60`, two genre matches available

**What changed and why it makes sense.**
Both profiles sit in the "moderate energy" band, but the pop listener's experience is
noticeably better. The jazz lover has exactly one genre match in the catalog
(Coffee Shop Stories); after that, every remaining song scores zero on both genre and
mood, so the list degrades to a pure energy sort. The pop listener has two genre
matches (Sunrise City and Gym Hero) and one partial mood match (Rooftop Lights /
indie pop), giving the top three real signal.

This comparison most clearly illustrates the *genre representation bias*: jazz, with
one catalog entry, produces a thin, energy-sorted tail after position #1. Pop, with
two entries, sustains meaningful recommendations further down the list. The quality
of a user's experience is directly proportional to how many times their genre appears
in the catalog, not how well-defined their taste is.