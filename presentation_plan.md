# Presentation Plan: Merlin UK Geographic Customer Opportunity Segmentation

## Overview
This plan maps the completed analytical work (EDA notebook, segmentation model, opportunity scoring, dataset documentation, and Streamlit chatbot) onto the exact deliverables requested in the brief. The deck is designed to be **concise, executive-friendly, and commercially actionable**.

**Target length:** 3–4 slides total (Title + 2 core content slides + optional Appendix). This respects the brief's emphasis on clarity over complexity while still delivering impact.

---

## Slide 1: Title Slide

**Purpose:** Set context immediately.

**Content:**
- **Title:** Geographic Customer Opportunity Segmentation for Merlin UK
- **Subtitle:** Identifying high-potential areas, customer archetypes, and activation strategies using publicly available UK demographic data
- **Your name / role**
- **Date**
- **One-line summary:** "We found four distinct customer segments across 6,856 UK MSOAs and matched them to 23 Merlin attractions using propensity × proximity scoring."

**Design tip:** Include a small UK map thumbnail showing the four cluster colours (if you have plotted them in the notebook) as a visual anchor.

---

## Slide 2: Technical Approach

**Purpose:** Explain what was built, why, and what the limitations are. The brief explicitly asks for this as a single slide covering data sources, geography, features, methodology, scoring logic, and assumptions.

**Layout suggestion:** Split into 4 quadrants or a 2×2 grid to fit density without clutter.

**Content:**

### Top Left — Data Sources & Geography
- **Sources:** UK Census 2021 (age, household composition), ONS IMD 2025 (deprivation/income), ONS MSOA Centroids, Experian net disposable income, public Merlin attraction locations.
- **Geographic level:** **MSOA** (~7,264 England/Wales areas, ~5,000–15,000 people each). Chosen because it balances granularity with statistical reliability — finer than LADs for media targeting, coarser than postcodes for data availability.

### Top Right — Feature Engineering & Clustering
- **Features used:** 11 scaled features: net disposable income, IMD, child deprivation (IDACI), housing/service barriers, and 7 derived household/age proportions (children 0–14, young adults 20–34, older adults 65+, households with dependent children, couples with children, lone parents, one-person households).
- **Methodology:** K-Means clustering (K=4 selected via silhouette score). Chosen for speed, interpretability, and the fact that it forces every area into a segment — useful for national media planning.
- **Collinearity check:** Income and IMD are moderately correlated; household proportions and child counts are correlated — but all were retained because each carries distinct commercial meaning (e.g., "stable couple with kids" vs "lone parent with kids").

### Bottom Left — Opportunity Scoring Logic
- **Formula:** `opportunity_score = segment_fit × distance_decay`
  - *Segment fit:* Pre-defined 0–1 propensity matrix mapping each cluster to each attraction type (e.g., Affluent Nuclear Families = 1.0 for LEGOLAND, 0.2 for Madame Tussauds).
  - *Distance decay:* Exponential decay `exp(-distance_km / decay_km)` with attraction-specific catchment assumptions (resorts ~90 km, city flagships ~40 km, coastal SEA LIFE ~70 km).
- **Output:** `opportunity_score_100` normalised per attraction so the top MSOA for each attraction always scores 100.

### Bottom Right — Assumptions & Limitations
- Distance is **straight-line (Haversine)**, not drive-time — rural or water-separated areas may be overestimated.
- Income/deprivation are **MSOA-level modelled estimates**, not household-level truth.
- **No actual Merlin visitor or transaction data** — this is a *prospective* segmentation based on demographic propensity and proximity.
- Competitive landscape (e.g., Paultons Park, Drayton Manor) is **not accounted for**.
- Scotland data is partial — some deprivation and income datasets cover England/Wales only.

---

## Slide 3: Business Insights & Activation

**Purpose:** Summarise what to do with the segmentation. The brief explicitly asks for this as a single slide covering key opportunity areas, segment characteristics, attraction alignment, and media activation.

**Layout suggestion:** Left half = segment portraits; Right half = activation map / top recommendations.

**Content:**

### Left Column — The Four Customer Segments
Present as four colour-coded "cards" or a 2×2 grid. Each card contains:

| Segment | % of MSOAs | Income | Defining Trait | Primary Resonance |
|---------|-----------|--------|----------------|-------------------|
| **0 — Affluent Nuclear Families** | 30% | £48.7k | 32% households with kids, 23% stable couples with kids | **Resorts:** LEGOLAND, Alton Towers, Chessington, Warwick Castle |
| **1 — Comfortable Empty Nesters** | 36% | £38.1k | 25% aged 65+, 31% one-person households, very few kids | **Heritage & City:** Warwick Castle, London Eye, Madame Tussauds, midweek breaks |
| **2 — Struggling Young Families** | 25% | £35.2k | 21% children (highest), 34% households with kids, high deprivation | **Value Day Trips:** SEA LIFE, Cadbury World, Chessington (with discount messaging) |
| **3 — Urban Young Professionals** | 8% | £44.9k | 36% young adults, 38% one-person households, few kids | **City Experiences:** London Eye, Madame Tussauds, Dungeon, Thorpe Park |

**Key insight to call out:** Two clusters have virtually identical income (~£48k) but are separated entirely by life stage. This is not a "rich vs poor" map — it is a **lifecycle** map. That is what makes it commercially useful.

### Right Column — Activation Recommendations
Present as 3–4 concrete, prioritised actions:

1. **Premium Resort Push (Cluster 0)**
   - Target affluent family MSOAs within 60–90 km of LEGOLAND, Alton Towers, and Chessington.
   - Activation: Hotel + ticket bundles, annual pass family plans, school-holiday digital campaigns.
   - Media: Facebook/Instagram family targeting, programmatic geo-fencing around competitor resorts.

2. **Value Volume Unlock (Cluster 2)**
   - Biggest growth opportunity: high latent demand (lots of kids) but price-sensitive.
   - Activation: "Kids Go Free" at SEA LIFE and Discovery Centres, payment-plan annual passes, high-street voucher partnerships (Tesco Clubcard, Meerkat Movies style).
   - Media: Local radio, digital out-of-home near retail parks, TikTok value creators.

3. **Urban Experience Economy (Cluster 3)**
   - Highly concentrated in London, Manchester, Birmingham cores.
   - Activation: Experience gifts (Christmas/Valentine's), influencer partnerships, student discounts, evening events.
   - Media: TikTok/Instagram Reels, commuter Tube/DLR digital posters, Spotify geo-targeted audio.

4. **Underpenetrated Regions**
   - Rural Wales, South West beyond Bristol, North East England, Scotland outside Edinburgh.
   - High family or young-adult populations but >100 km from nearest resort.
   - Activation: Pop-up events (e.g., LEGOLAND touring experience), digital awareness campaigns, future site evaluation data.

### Bottom Banner — Example Business Questions Answered
Add a single line or small text box:
> *"Which areas are highest opportunity for LEGOLAND?" → Home Counties MSOAs with Cluster 0 profile within 40 km of Windsor.*
> *"Where should Merlin target family annual passes?" → Cluster 2 MSOAs within 30 km of a SEA LIFE or Discovery Centre, with "payment plan" messaging.*
> *"Which regions appear underpenetrated?" → High-Cluster-2 rural areas in Wales and the North East, where distance to any resort exceeds 80 km.*

---

## Slide 4 (Optional): The Interface — Demo Screenshot

**Purpose:** Show the bonus deliverable (Streamlit chatbot) without making the deck feel like a "tech pitch."

**Content:**
- One screenshot of the Streamlit app running with an example query and response.
- Caption: *"A lightweight natural-language interface lets commercial teams query the dataset directly — no SQL or Python required. Example: 'Which areas are highest opportunity for LEGOLAND?' returns top MSOAs with scores and activation recommendations instantly."*
- **Link:** `github.com/...` or `streamlit run main.py` instructions if submitting code.

**Note:** Only include this if you have a working screenshot. If the app is not yet running locally, omit this slide and mention the interface in the supporting documentation instead.

---

## Slide 5 (Optional): Appendix / Deep-Dive

**Purpose:** Provide backup detail for technical questions.

**Content (pick 1–2):**
- **Cluster profile table:** The mean feature values per cluster (the table you already generated in the notebook).
- **Top 10 MSOAs per attraction:** A small table or heatmap snippet.
- **Silhouette vs Elbow plot:** Evidence that K=4 was selected rigorously.
- **Geographic distribution map:** A choropleth of `cluster_name` across the UK.

**Design tip:** Label this "Appendix — For Discussion" so executives know they can skip it unless asked.

---

## Speaker Notes & Narrative Arc

When presenting, use this 3-minute narrative flow:

1. **Hook (15 sec):** *"Merlin has 23 UK attractions, but not every area is equally valuable. We built a segmentation that tells you which 1,000 MSOAs to prioritise — and exactly what message to send them."*

2. **How (60 sec, Slide 2):** Walk through data sources, MSOA level, K=4 clustering, and the propensity × distance formula. Emphasise the **lifecycle insight** (same income, different life stage = different attraction).

3. **So What (90 sec, Slide 3):** Go through the four segments rapidly, then spend the most time on **activation recommendations** — this is what the brief rewards. End with the underpenetrated regions insight because it shows strategic thinking beyond the existing estate.

4. **Proof (15 sec):** Mention the CSV output and the chatbot interface. *"Everything is queryable — the model doesn't sit in a Jupyter notebook, it sits in a tool the business can use."*

---

## Assets to Prepare

Before building the slides, extract or create these visuals from your notebook/code:

1. **UK choropleth map** of the four clusters (use `geopandas` + `matplotlib` or `plotly`). This is the single most impactful visual.
2. **Cluster mean table heatmap** — the silhouette/profile data rendered as a coloured table.
3. **Opportunity score map** — pick one attraction (e.g., LEGOLAND) and plot `opportunity_score_100` geographically.
4. **Streamlit screenshot** — if you can get the app running, take one screenshot of a query + response.
5. **CSV file** — already exists: `msoa_attraction_opportunities.csv`. Ensure it is included in the submission zip.

---

## Submission Checklist

- [ ] Presentation slides (PDF or PowerPoint) — 3–4 slides max
- [ ] Supporting data output — `msoa_attraction_opportunities.csv`
- [ ] Optional code repository — `eda.ipynb`, `main.py`, `dataset_documentation.md`, `pyproject.toml`
- [ ] README or cover note explaining how to run `streamlit run main.py`
