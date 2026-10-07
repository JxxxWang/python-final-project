# Presentation Script (≈10 minutes)

Slides: `notebooks/presentation.ipynb` (RISE / `jupyter nbconvert --to slides --post serve`) · Static export: `notebooks/presentation.slides.html`
Timing is cumulative; ~140 words per minute.

---

## Slide 1 — Title (0:00–0:20)
"Hi everyone. Our project predicts whether a *new* user of a data-science platform will still be active in their second month, using only what they did in their signup month. It comes from the Zindi New User Engagement challenge, and the metric is F1 on the 'active' class."

## Slide 2 — Problem and importance (0:20–1:10)
"The platform hosts competitions, blogs, jobs and discussions. It gets thousands of signups, but only about one in five is active the following month. Re-engagement is costly: emails, push notifications, onboarding help. If we can rank new users by their risk of leaving, one month ahead, we spend that budget where it can still work, cut wasted messages, lift activation, and learn which first-month behaviours matter. Technically this is a binary classification task with roughly 1-to-4 imbalance, which is why we use F1 rather than accuracy."

## Slide 3 — Loading and X/y split (1:10–2:00)
"We read all nine CSVs with pandas, about 12,400 users and 317 thousand activity rows. The target y is one if the user has *any* event — click, competition join, post or comment — in the month after signup. Features X use *only* signup-month events, so there is no look-ahead. Labels for April signups are hidden — that's the test set — and May has no next month, so we train on the 9,026 users who signed up from November to March."

## Slide 4 — Data preparation (2:00–3:10)
"Each transformation has a reason. The target merges four tables into one binary variable. Features are event counts per activity, zero-filled because 'never did it' is information. Categorical columns — FeatureX, FeatureY and country — are one-hot encoded for logistic regression and integer-coded for trees. Country is missing for 47 percent of users; we keep that as its own 'unknown' category instead of dropping half the data. We derive signup hour and day from the timestamp, and we aggregate page-specific clicks into page types, which I'll justify in a moment. Counts are standardised only for logistic regression."

## Slide 5 — EDA 1: suspicious labels (3:10–4:20)
"Now the exploratory analysis with seaborn. This chart shows the next-month active rate by signup cohort. Four cohorts sit between 12 and 21 percent, and the test set is around 14 percent. But December signups are at 78 percent. This was visible earlier too: an 'all active' predictor scored 0.47 in our cross-validation but only 0.25 on the leaderboard. So something in December's label month inflates the target."

## Slide 6 — EDA 2: the culprit (4:20–5:20)
"Breaking December's active users down by what they did shows one anomaly: a record called badge_OCZE. 96 percent of the active December users have it, versus 5 percent in other cohorts, and half of December's users have *only* that one record. It was written 8,864 times, mostly on a single day, the 15th of one month, for about 3,000 users at once. That looks like a system bulk grant rather than user behaviour — an inference, since the organisers do not document it. We therefore drop it at load time."

## Slide 7 — EDA 3: fix and class balance (5:20–6:00)
"After the fix, December drops to 29 percent, in line with the other months; the all-ones F1 falls from 0.47 to 0.33, much closer to the leaderboard. The clean data has 19.6 percent positives, a 1-to-4 imbalance, which motivates class weighting later."

## Slide 8 — EDA 4: behavioural signal (6:00–6:50)
"Which behaviours matter? Users who create or update submissions, download data files or join competitions retain at 33–44 percent, roughly twice the 20 percent base rate. Overall activity volume is the strongest signal: heavy users with more than 25 events retain at 41 percent versus 3 percent for users with none. Profile columns and the missing-country flag carry only weak signal. So behaviour counts are the right backbone."

## Slide 9 — EDA 5: new pages (6:50–7:30)
"One more finding that shaped feature design. Competitions and blogs change every month. Counting views per specific page, 29 percent of April competition views and 53 percent of job views fall on columns the training data never saw. If instead we count per page *type*, all April views land on well-supported columns, and the feature matrix shrinks from 390 to 45 columns."

## Slide 10 — Evaluation design (7:30–8:20)
"For evaluation, we use F1 of the active class, the competition metric, and compare against all-ones at 0.328. We use five-fold cross-validation, stratified by label and grouped by user, with a fixed seed so every model sees the same folds. For tuning we grid-search 216 decision-tree configurations — depth, leaf size, criterion, class weights — and run that search *inside* every outer training fold, a nested cross-validation, so the reported score isn't inflated by tuning. The 0.5 threshold is fixed to keep experiments comparable."

## Slide 11 — Models and results (8:20–9:20)
"Results. Plain logistic regression gets 0.375: it flags only 9 percent of users, too conservative for a 1-to-4 problem. Class weighting raises it to 0.475. The default decision tree overfits badly — training F1 of 0.995 versus 0.39 validation. Tuning cuts depth to 5 to 8 and gives 0.456, and page-type features give 0.469 with a simpler tree. The heatmap shows a clear sweet spot at depth 4 to 5. Every model beats the baseline, and the two best are about 0.47–0.48, with a standard deviation near 0.01."

## Slide 12 — Analysis, applicability, impact (9:20–10:00)
"What does this mean in practice? The weighted logistic regression flags 31 percent of users, with 39 percent precision — twice the base rate — and catches 61 percent of those who will stay. In a toy campaign of 10,000 users, nudging everyone costs about five dollars per retained user reached, versus about two fifty when using the model's picks. So it solves the *prioritisation* problem, but with modest absolute precision it should drive cheap actions, not costly ones. The biggest lesson is that the data issue mattered more than the model: removing the leaked badge, class weights and depth control were bigger wins than model choice. Limitations: random-split CV mixes months, so a time-based split is next; the threshold should be tuned for the actual campaign cost; and the leaderboard check is pending. Thank you — happy to take questions."

---

## Rubric checklist
| Rubric item | Slide(s) |
|---|---|
| Problem, importance, how ML helps (4) | 2, 12 |
| pandas load, X / y split (2) | 3 |
| Encoding, missing values, new features, target prep with motivation (5) | 3, 4 |
| Seaborn EDA with patterns driving decisions (4) | 5–9 |
| CV procedure, metric, model, hyper-parameter search (7) | 10, 11 |
| Analysis, applicability, conclusion, impact (8) | 12 |
| Structure & clarity (10) | Problem → Data → Prep → EDA → Eval → Results → Impact |
