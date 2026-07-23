# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Mini Vibify v0.1

---

## 2. Intended Use  

Mini Vibify recommends songs from a small catalog using a user's stated genre, mood, and audio preferences. It is intended for classroom exploration, not real-world deployment.

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The model awards points for matching genre and mood, then rewards songs whose energy, tempo, and acousticness are close to the user's targets. The total score determines the ranking, and matching features become the explanation.

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

The catalog contains 17 songs with genre, mood, energy, tempo, valence, danceability, and acousticness fields. Seven songs were added to broaden the starter data; lyrics, language, history, popularity, and cultural context are not included.

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

The system is easy to understand because every score has visible reasons. It works best for clear profiles such as chill lofi or intense rock, where genre, mood, and numerical preferences agree.

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The recommender can create a filter bubble because exact genre and mood matches
receive fixed bonus points, so songs from unfamiliar genres may be pushed down
even when their audio features are a strong match. The catalog is also small and
uneven: lofi has three songs, while several genres and moods have only one, so
those categories cannot be represented reliably. The energy-gap rule assumes a
single target energy and may underserve users whose tastes change by activity or
who prefer a broad range of energy levels. The model uses metadata only and may
miss important preferences expressed through lyrics, culture, language, or artist
familiarity.

---

## 7. Evaluation 

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I compared the output for each pair of test profiles:

- **High-Energy Pop vs. Chill Lofi:** High-Energy Pop puts upbeat pop songs such
  as `Sunrise City` first, while Chill Lofi puts quiet lofi songs such as
  `Library Rain` first. This makes sense because the profiles disagree on genre,
  mood, energy, and tempo.
- **High-Energy Pop vs. Deep Intense Rock:** Both profiles favor energetic music,
  so they share some songs near the top. Pop ranks `Sunrise City` first because
  its genre and happy mood match; rock ranks `Storm Runner` first because its
  rock genre and intense mood match.
- **High-Energy Pop vs. Conflicting Preferences:** The conflicting profile asks
  for sad blues but also very high energy. `Blue Neon` wins because its blues and
  sad labels earn strong match points, even though its energy is not as high as
  requested. This shows that categorical matches can outweigh a numerical gap.
- **Chill Lofi vs. Deep Intense Rock:** Chill Lofi favors slow, acoustic songs,
  while Deep Intense Rock favors fast, energetic songs. Their top results are
  different because the energy and tempo targets point in opposite directions.
- **Chill Lofi vs. Conflicting Preferences:** Both profiles can reward acoustic
  songs, but Chill Lofi favors low energy and the conflicting profile favors high
  energy. The same acoustic song can therefore score well for different reasons,
  but it will rank differently for each user.
- **Deep Intense Rock vs. Conflicting Preferences:** Both prefer high energy, so
  energetic tracks appear in both lists. Rock gets `Storm Runner` because of its
  genre and intense mood, while the conflicting profile gets `Blue Neon` because
  of its blues and sad labels.

`Gym Hero` sometimes appears for a user who wants happy pop because it matches
 the pop genre and has energy close to the user's target. It does not match the
 happy mood, but the scoring rule gives genre and energy enough points to keep
 it competitive. This is a useful reminder that a recommendation can be
 numerically strong without matching every part of a person's taste.

I also tested the weight-shift and mood-removal experiments. Increasing the
energy weight moved more high-energy songs upward, while removing mood made the
results less sensitive to emotional preference. These are qualitative checks,
not formal accuracy measurements, because the catalog has only 17 songs and no
ground-truth user ratings.

---

## 8. Future Work  

If I continued developing Mini Vibify, I would:

1. Add more songs and features such as loudness, instrumentalness, duration, and
   lyrics so recommendations had richer musical context.
2. Collect user feedback and tune the feature weights instead of choosing them
   manually.
3. Add diversity rules so the top results do not repeat the same artist or genre.

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

My biggest learning moment was seeing that a recommender is not magic: it is a
clear set of choices about which features matter and how much they count. AI
tools helped me draft scoring ideas, generate test profiles, and explain Python
patterns such as `sorted()`, but I had to double-check the CSV types, score math,
and actual rankings by running the program. I was surprised that a simple
weighted score could still feel like a recommendation because small differences
in genre, mood, and energy produced noticeably different lists. If I extended the
project, I would add feedback-based weight tuning and test the system with a
larger, more balanced catalog.

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
