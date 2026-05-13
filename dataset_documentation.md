# Merlin UK Geographic Customer Opportunity Segmentation — Dataset & Agent Context

## 1. Dataset Overview

This dataset contains a geographic customer opportunity segmentation for Merlin Entertainments UK. It is built at **MSOA (Middle Layer Super Output Area)** level — roughly 8,000 areas covering the whole UK, each representing ~5,000–15,000 people. Every row represents one MSOA and its associated demographic profile, cluster assignment, distances to Merlin attractions, and calculated opportunity scores. 

**Primary data sources:**
- UK Census 2021 (age structure, household composition)
- ONS Index of Multiple Deprivation (IMD) and sub-domain scores
- ONS Postcode Directory / MSOA centroid lookups (latitude, longitude)
- Merlin UK public attraction location data (latitude, longitude)
- ONS income proxies where available

**What the dataset can answer:**
- Which geographic areas are highest opportunity for a specific Merlin attraction
- Which customer segment an area belongs to and why
- How far each area is from every attraction
- What marketing activation strategy fits each area
- Where Merlin is underpenetrated versus where it already has natural demand

---

## 2. Complete Column Reference

This section lists **every column** in `msoa_attraction_opportunities.csv` exactly as it appears, grouped by category. The agent MUST use these exact names when writing pandas code.

### 2A. Geographic Identifiers
| Column | Meaning | Example |
|--------|---------|---------|
| `geography_code` | Unique MSOA identifier | E02000001 |
| `geography` | Local Authority District name | City of London |
| `latitude_msoa` | MSOA centroid latitude | 51.519151 |
| `longitude_msoa` | MSOA centroid longitude | -0.094693 |

### 2B. Raw Age Structure (counts)
| Column | Meaning |
|--------|---------|
| `age_total` | Total population in MSOA |

### 2C. Deprivation & Income
| Column | Meaning | Direction of Opportunity |
|--------|---------|--------------------------|
| `net_annual_disposable_income` | Estimated household disposable income | **Higher = more spending power** |
| `income_score_rate_weighted_avg` | ONS income deprivation score | **Lower = more attractive** |
| `index_of_multiple_deprivation_imd_score_weighted_avg` | Overall deprivation score (0–100, higher = more deprived) | **Lower = more attractive** |
| `income_deprivation_affecting_children_index_idaci_score_rate_weighted_avg` | Child income deprivation (0–1, higher = more deprived) | **Lower = affluent families with kids** |
| `income_deprivation_affecting_older_people_idaopi_score_rate_weighted_avg` | Older-person income deprivation (0–1, higher = more deprived) | **Lower = affluent older adults** |
| `barriers_to_housing_and_services_score_weighted_avg` | Geographic barriers / urban-rural accessibility proxy | Context-dependent: low = urban/accessible, high = rural/remote |

### 2D. Raw Household Composition (counts)
| Column | Meaning |
|--------|---------|
| `does_not_apply` | Household type not applicable / not classified |
| `one_person_aged_66_plus` | Single-person household, occupant 66+ |
| `one_person_other` | Single-person household, younger adult |
| `cohabiting_couple_no_children` | Unmarried couple, no children |
| `cohabiting_couple_dep_children` | Unmarried couple, dependent children |
| `cohabiting_couple_non_dep_children` | Unmarried couple, non-dependent children |
| `married_couple_no_children` | Married/civil partnership, no children |
| `married_couple_dep_children` | Married/civil partnership, dependent children |
| `married_couple_non_dep_children` | Married/civil partnership, non-dependent children |
| `lone_parent_dep_children` | Single parent, dependent children |
| `lone_parent_non_dep_children` | Single parent, non-dependent children |
| `single_family_aged_66_plus` | Multi-person family, all aged 66+ |
| `other_household_dep_children` | Other household type with dependent children |
| `other_household_other_family` | Other related household |
| `other_household_students_66_plus` | Students or all occupants 66+ |

### 2E. Derived Household Proportions
| Column | Meaning | Used in Clustering? |
|--------|---------|-------------------|
| `total_households` | Sum of all household types | No (denominator) |
| `prop_children_0_14` | Children 0–14 / total population | Yes |
| `prop_teenagers_15_19` | Teenagers 15–19 / total population | Yes |
| `prop_young_adults_20_34` | Young adults 20–34 / total population | Yes |
| `prop_family_core_25_49` | Adults 25–49 / total population | No (post-hoc index) |
| `prop_older_adults_65_plus` | Adults 65+ / total population | Yes |
| `prop_households_with_dep_children` | Households with dependent children / total households | Yes |
| `prop_couples_with_dep_children` | Couples with dependent children / total households | Yes |
| `prop_lone_parent` | Lone-parent households / total households | No (context) |
| `prop_one_person_households` | Single-person households / total households | Yes |
| `prop_retired_households` | Retired households / total households | No (context) |

### 2F. Cluster Assignment
| Column | Meaning |
|--------|---------|
| `cluster` | Numeric cluster label (0–3) |
| `cluster_name` | Human-readable cluster name: `Affluent Nuclear Families`, `Comfortable Empty Nesters`, `Struggling Young Families`, `Urban Young Professionals` |

### 2G. Attraction, Distance & Opportunity
| Column | Meaning |
|--------|---------|
| `attraction_name` | Full Merlin attraction name |
| `latitude_attraction` | Attraction latitude |
| `longitude_attraction` | Attraction longitude |
| `distance_km` | Haversine distance from MSOA centroid to attraction (km) |
| `opportunity_score` | Raw score = segment_fit × distance_decay (0–1 scale, unnormalised) |
| `opportunity_score_100` | Normalised opportunity score (0–100) **per attraction** — top MSOA for each attraction = 100 |
| `activation_recommendation` | Pre-calculated marketing activation strategy for this MSOA–Attraction pair |

**Agent guidance:** When users ask about "areas", "regions", or "postcodes", translate to `geography` (Local Authority District name) or `geography_code` (MSOA). These are the two geographic levels available.

---

## 3. Core Demographic & Deprivation Features

| Column | Meaning | Direction of Opportunity |
|--------|---------|--------------------------|
| `net_annual_disposable_income` | Estimated household disposable income | **Higher = more spending power** |
| `index_of_multiple_deprivation_imd_score_weighted_avg` | Overall deprivation score (0–100 scale, higher = more deprived) | **Lower = more attractive** |
| `income_deprivation_affecting_children_index_idaci_score_rate_weighted_avg` | Child poverty / income deprivation affecting children (0–1, higher = more deprived) | **Lower = affluent families with kids** |
| `barriers_to_housing_and_services_score_weighted_avg` | Geographic barriers / urban-rural accessibility proxy | Context-dependent: low = urban/accessible, high = rural/remote |

**Agent guidance:** Do NOT tell users that high IMD or high IDACI is "good." These are deprivation scores — high values mean disadvantage. Affluent family opportunity is signalled by **high income + low IDACI**.

---

## 4. Household Composition Features

These are raw counts of households by type. For clustering, they were converted into **proportions** (see Section 5).

| Column | Meaning |
|--------|---------|
| `one_person_aged_66_plus` | Single-person household, occupant 66+ |
| `one_person_other` | Single-person household, younger adult |
| `cohabiting_couple_no_children` | Unmarried couple, no children |
| `cohabiting_couple_dep_children` | Unmarried couple, dependent children |
| `cohabiting_couple_non_dep_children` | Unmarried couple, non-dependent (grown-up) children |
| `married_couple_no_children` | Married/civil partnership, no children |
| `married_couple_dep_children` | Married/civil partnership, dependent children |
| `married_couple_non_dep_children` | Married/civil partnership, non-dependent children |
| `lone_parent_dep_children` | Single parent, dependent children |
| `lone_parent_non_dep_children` | Single parent, non-dependent children |
| `single_family_aged_66_plus` | Multi-person family, all aged 66+ |
| `other_household_dep_children` | Other household type with dependent children |
| `other_household_other_family` | Other related household |
| `other_household_students_66_plus` | Students or all occupants 66+ |

---

## 5. Derived Proportion Features (Used in Clustering)

These proportions were the actual inputs to the clustering model.

| Feature | Calculation | Business Meaning |
|---------|-------------|------------------|
| `prop_children_0_14` | Children aged 0-14 / total population | Family attraction demand |
| `prop_teenagers_15_19` | Teenagers 15-19 / total population | Thrill park / teen audience |
| `prop_young_adults_20_34` | Young adults 20-34 / total population | Urban professional / student audience |
| `prop_older_adults_65_plus` | Adults 65+ / total population | Empty nester / retiree audience |
| `prop_households_with_dep_children` | Households with dependent children / total households | Core family market size |
| `prop_one_person_households` | Single-person households / total households | Urban / professional / lone adult signal |
| `prop_couples_with_dep_children` | Married or cohabiting couples with dependent children / total households | Stable nuclear family signal |

**Agent guidance:** When interpreting clusters, always reference these proportions, not raw counts. A rural MSOA and an urban MSOA may have the same number of children, but very different **concentrations** of children.

---

## 6. The Four Customer Segments (Clusters)

These segments were derived using K-Means clustering on scaled demographic features. Every MSOA belongs to exactly one segment.

### Cluster 0 — Affluent Nuclear Families
| Metric | Typical Value | Interpretation |
|--------|---------------|----------------|
| Disposable income | ~£48,700 | Highest spending power |
| IMD | ~12 | Very low deprivation |
| IDACI | ~0.22 | Low child poverty = financially secure families |
| Children 0-14 | ~18% | High share of young children |
| Households with dependent children | ~32% | Highest proportion of family households |
| Couples with dependent children | ~23% | Stable, two-parent family structure |
| Older adults 65+ | ~18% | Moderate |

**Commercial profile:** This is Merlin's premium core market. They have the money for resort hotels, short breaks, and premium annual passes. Predominantly suburban Home Counties and affluent commuter belts.
**Best attraction fit:** LEGOLAND Windsor, Alton Towers, Chessington, Warwick Castle, Cadbury World.
**Activation:** Premium resort bundles, hotel upsells, school-holiday campaigns, annual pass family plans.

---

### Cluster 1 — Comfortable Empty Nesters
| Metric | Typical Value | Interpretation |
|--------|---------------|----------------|
| Disposable income | ~£38,100 | Moderate, financially stable |
| IMD | ~17 | Low deprivation |
| IDACI | ~0.28 | Moderate child poverty (but few children present) |
| Children 0-14 | ~15% | Lowest share of children |
| Households with dependent children | ~24% | Low |
| Older adults 65+ | ~25% | **Highest** — dominated by retirees/empty nesters |
| One-person households | ~31% | High lone-person / widow(er) presence |

**Commercial profile:** No young children at home. Time-flexible, midweek availability, culturally oriented. Not thrill-seekers. Heritage and leisure over adrenaline.
**Best attraction fit:** Warwick Castle, The London Eye, Madame Tussauds, city SEA LIFE, Cadbury World (nostalgia).
**Activation:** Off-peak short breaks, midweek direct mail/email, grandparent annual passes, heritage storytelling.

---

### Cluster 2 — Struggling Young Families
| Metric | Typical Value | Interpretation |
|--------|---------------|----------------|
| Disposable income | ~£35,200 | Lowest spending power |
| IMD | ~39 | **Highest deprivation** |
| IDACI | ~0.57 | **Highest child poverty** — financially squeezed families |
| Children 0-14 | ~21% | **Highest** share of young children |
| Households with dependent children | ~34% | Very high family density |
| Couples with dependent children | ~19% | Lower stable-couple rate, more lone parents |
| Older adults 65+ | ~13% | Low |

**Commercial profile:** High latent demand (lots of kids) but price-sensitive. These are "would love to go but can't afford it" families. Biggest growth opportunity if reached with the right price point.
**Best attraction fit:** SEA LIFE centres (value day trips), Chessington, Cadbury World, LEGOLAND Discovery Centres (cheaper than resorts), Alton Towers (with value positioning).
**Activation:** "Kids Go Free", annual pass payment plans, high-street voucher partnerships, local radio/digital, advance-book discounts, budget resort packages.

---

### Cluster 3 — Urban Young Professionals
| Metric | Typical Value | Interpretation |
|--------|---------------|----------------|
| Disposable income | ~£44,900 | Second-highest spending power |
| IMD | ~24 | Moderate deprivation (inner-city inequality) |
| IDACI | ~0.42 | Moderate child poverty (but few children) |
| Young adults 20-34 | ~36% | **Highest** — dominated by millennials/Gen Z |
| One-person households | ~38% | **Highest** — urban singles and flat-sharers |
| Children 0-14 | ~13% | Lowest share of children |
| Older adults 65+ | ~10% | Lowest |
| Teenagers 15-19 | ~7% | Noticeable teen presence |

**Commercial profile:** Experience-driven, socially motivated, high disposable income per person (no kids), low brand loyalty unless influenced. Instagram/TikTok natives.
**Best attraction fit:** The London Eye, Madame Tussauds, The London Dungeon, Shrek's Adventure, Thorpe Park, city SEA LIFE.
**Activation:** Social/Instagram campaigns, influencer partnerships, experience gifts, student/youth discounts, off-peak dating/event nights, commuter digital out-of-home.

---

## 7. Merlin Attractions in the Dataset

The dataset contains Haversine distances (in kilometres) from every MSOA centroid to each of the following attractions. Distances are straight-line (crow flies), not drive-time.

### By Attraction Type & Catchment Behaviour

| Attraction Name | Short Type | Decay Characteristic | Typical Audience |
|-----------------|------------|----------------------|------------------|
| LEGOLAND® Windsor Resort | `legoland` | Wide resort draw (~90 km) | Families with young children |
| LEGOLAND® Discovery Centre Birmingham | `legoland` | Indoor local draw (~55 km) | Young families, rainy-day |
| LEGOLAND® Discovery Centre Manchester | `legoland` | Indoor local draw (~55 km) | Young families, rainy-day |
| Alton Towers Resort | `alton_towers` | Wide resort draw (~95 km) | Thrill-seeking families/teens |
| Chessington World Of Adventures Resort | `chessington` | Wide resort draw (~85 km) | Families, mixed ages |
| Thorpe Park | `thorpe_park` | Mixed suburban draw (~75 km) | Teens, young adults, thrill-seekers |
| Warwick Castle | `warwick_castle` | Wide heritage draw (~85 km) | Families, empty nesters, schools |
| Cadbury World | `cadbury_world` | Wide draw (~75 km) | Families, nostalgia, chocolate tourism |
| Madame Tussauds London | `madame_tussauds` | City/tourist draw (~40 km) | Tourists, young professionals |
| The London Eye | `london_eye` | City/tourist draw (~40 km) | Tourists, young professionals, dates |
| The London Dungeon | `dungeon` | City/tourist draw (~40 km) | Young adults, thrill-seekers |
| The York Dungeon | `dungeon` | Regional city draw (~50 km) | Young adults, heritage thrill |
| The Edinburgh Dungeon | `dungeon` | Regional city draw (~50 km) | Young adults, heritage thrill |
| Shrek's Adventure! London | `shrek_adventure` | City/family draw (~40 km) | Young families, tourists |
| SEA LIFE London | `sea_life` | City draw (~45 km) | Tourists, families, dates |
| National SEA LIFE Centre Birmingham | `sea_life` | City draw (~55 km) | Local families |
| SEA LIFE Manchester | `sea_life` | City draw (~55 km) | Local families |
| SEA LIFE Brighton | `sea_life` | Coastal draw (~60 km) | Families, day-trippers |
| SEA LIFE Blackpool | `sea_life` | Coastal draw (~70 km) | Families, holidaymakers |
| SEA LIFE Great Yarmouth | `sea_life` | Coastal draw (~70 km) | Families, holidaymakers |
| SEA LIFE Scarborough | `sea_life` | Coastal draw (~70 km) | Families, holidaymakers |
| SEA LIFE Weymouth Adventure Park | `sea_life` | Coastal/resort draw (~70 km) | Families, adventure park combo |
| SEA LIFE Sanctuary Hunstanton | `sea_life` | Coastal draw (~75 km) | Families, nature-oriented |
| SEA LIFE Loch Lomond | `sea_life` | Rural destination draw (~80 km) | Tourists, nature families |

**Agent guidance:** When a user asks about "SEA LIFE", ask for clarification or aggregate across all SEA LIFE locations. Each SEA LIFE has a different catchment (city vs coastal vs rural) and therefore different high-opportunity MSOAs. Do not assume SEA LIFE London is the only SEA LIFE.

---

## 8. Opportunity Scoring Logic

### How the score is calculated

For every MSOA–Attraction pair, the opportunity score is:

```
opportunity_score = segment_fit × distance_decay
```

Where:
- **segment_fit** (0–1): How naturally the MSOA's cluster segment matches the attraction type. See Section 6 for the fit matrix. Affluent Nuclear Families have 1.0 fit for LEGOLAND Windsor, but only 0.15 fit for Madame Tussauds.
- **distance_decay** (0–1): How proximity boosts opportunity. Calculated as `exp(-distance_km / decay_km)` where `decay_km` is attraction-specific. At 0 km, decay = 1.0. At the decay distance, decay ≈ 0.37.

The final `opportunity_score_100` is normalised to a 0–100 scale **within each attraction**, so the highest-scoring MSOA for that attraction always scores 100.

### What the score means
- **90–100:** Exceptional opportunity — core target geography, high segment fit, close proximity. Prioritise media spend here.
- **70–89:** Strong opportunity — good fit and reasonable distance. Include in regional campaigns.
- **40–69:** Moderate opportunity — either a stretch in distance or a weaker segment match. Test with digital/lower-cost channels.
- **15–39:** Weak opportunity — significant distance or poor segment fit. Avoid paid media.
- **<15:** Very low priority — unlikely to convert efficiently.

**Agent guidance:** Opportunity scores are RELATIVE within an attraction, not absolute across attractions. An MSOA scoring 80 for LEGOLAND and 75 for Alton Towers is strong for both, but the 80 means "top decile for LEGOLAND" while 75 means "top quartile for Alton Towers." Do not compare the raw numbers across different attractions as if they are directly comparable currency.

---

## 9. Key Business Rules & Activation Logic

Use these rules when users ask "What should we do in [area]?" or "How do we activate [segment]?"

| Cluster | If Attraction Type Is... | Activation Recommendation |
|---------|--------------------------|---------------------------|
| 0 (Affluent Nuclear Families) | Resort (LEGOLAND, Alton Towers, Chessington, Warwick Castle) | Premium resort & hotel bundles; annual pass upsell; school-holiday push |
| 0 | Cadbury World | Family day-trip premium; school-holiday push |
| 0 | SEA LIFE | Annual pass gateway; upsell to resort breaks |
| 0 | Thorpe Park | Teen-plus family thrill; summer campaign |
| 0 | City (London Eye, Madame Tussauds, Dungeon) | City experience add-on for short-break guests |
| 1 (Comfortable Empty Nesters) | Heritage (Warwick Castle, Cadbury World) | Heritage short-break; midweek direct mail; off-peak senior rates |
| 1 | SEA LIFE | Leisurely day out; off-peak senior rates |
| 1 | City (London Eye, Madame Tussauds) | City experience gift; theatre-break bundle |
| 1 | Dungeon | Adult heritage-edgy; group bookings |
| 2 (Struggling Young Families) | SEA LIFE | Value entry; Kids Go Free; local activation |
| 2 | LEGOLAND (Discovery) | Discovery centre entry; payment-plan passes |
| 2 | Resort (Chessington, Alton Towers, Cadbury World) | Value family bundles; advance-book discounts |
| 2 | Thorpe Park | Teen value thrill; group/student rates |
| 2 | City | High-street voucher partnership; budget positioning |
| 3 (Urban Young Professionals) | City (London Eye, Madame Tussauds, Dungeon) | Social/Instagram campaign; experience gift |
| 3 | Shrek's Adventure | Date-night / friend-group; TikTok activation |
| 3 | Thorpe Park | Thrill-seeker day-trip; influencer partnership |
| 3 | SEA LIFE | City date experience; evening events |
| 3 | Resort | Urban awareness only; commuter digital out-of-home |

---

## 10. How to Answer Common Query Types

### Query: "Which areas are highest opportunity for [Attraction]?"
**Approach:**
1. Filter to the exact attraction name (e.g., "LEGOLAND Windsor Resort").
2. Sort by `opportunity_score_100` descending.
3. Return the top N MSOAs, showing `lad24nm`, `cluster` name, `distance_km`, and `opportunity_score_100`.
4. Describe the pattern: e.g., "The top areas are affluent family suburbs within 30–50 km of Windsor."

### Query: "Where should Merlin target family annual passes?"
**Approach:**
1. Look for MSOAs where `cluster == 0` (Affluent Nuclear Families) OR `cluster == 2` (Struggling Young Families).
2. For cluster 0: recommend premium annual passes for resorts (LEGOLAND, Alton Towers) — areas with high income, low IDACI, close to a resort.
3. For cluster 2: recommend value annual passes or payment-plan passes — areas with high children, high IDACI (price-sensitive), close to a SEA LIFE or Discovery Centre.
4. Name specific LADs and explain the dual strategy (premium vs value).

### Query: "Which regions appear underpenetrated?"
**Approach:**
1. Underpenetrated means: high segment fit (lots of target customers) but currently low opportunity score due to **distance** (far from nearest attraction) OR low income/deprivation barriers.
2. Identify MSOAs with high `prop_children_0_14` or high `prop_young_adults_20_34` but `opportunity_score_100 < 30` for all nearby attractions.
3. Highlight regions like rural Wales, South West beyond Bristol, North East England, or Scotland outside Edinburgh — these have family or young-professional populations but limited Merlin presence.
4. Recommend: pop-up events, digital awareness campaigns, or future site evaluation.

### Query: "What segment is [Area Name]?"
**Approach:**
1. Look up `lad24nm` (or `geography_code`) in the dataset.
2. Read the `cluster` value and translate to the human-readable name from Section 6.
3. Cite the specific proportions and income that define that cluster to justify the label.
4. Mention which attraction types fit best and why.

### Query: "How far is [Area] from [Attraction]?"
**Approach:**
1. Look up the specific MSOA or LAD.
2. Report the exact `distance_km` for that attraction.
3. Provide context: compare to the attraction's typical decay distance (e.g., "At 65 km, this is within the typical catchment for a coastal SEA LIFE but at the edge of a city attraction's draw").

---

## 11. Assumptions & Limitations

**Must be stated when users ask about model confidence or data quality:**

1. **Distance is straight-line (Haversine), not drive-time.** A 40 km straight-line distance across the Pennines or through London traffic can be materially longer in practice. Areas separated by water (e.g., near the Mersey or Thames estuary) may appear closer than they actually are.
2. **Clusters are socioeconomic, not geographic.** Two MSOAs in the same cluster may be hundreds of miles apart (e.g., Surrey and Cheshire both have Affluent Nuclear Families). Geographic coherence must be checked separately.
3. **Income and deprivation data are modelled/weighted averages at MSOA level, not household-level truth.** They are reliable for ranking and segmentation but should not be quoted as exact figures for individual families.
4. **Opportunity scores are relative per attraction.** A score of 80 for LEGOLAND and 70 for Alton Towers does not mean LEGOLAND is "better" in absolute terms — it means the MSOA is in a higher percentile for LEGOLAND's specific distribution.
5. **No actual visitor or transaction data is included.** This is a *prospective* segmentation based on population propensity and proximity. It assumes that demand follows demography, which is directionally true but not perfectly predictive.
6. **Attraction-specific decay constants are assumptions based on UK leisure market norms.** They are not calibrated against actual ticket sales or postcode data.
7. **Cadbury World is included as a Merlin-adjacent attraction** (Mondelez licensing). Its fit scores reflect family chocolate-tourism appeal, not pure theme-park thrill appeal.
8. **The model does not account for competitive overlap.** An area high-opportunity for LEGOLAND may also be high-opportunity for Paultons Park or Chessington; it does not adjust for market share.

---

## 12. Quick Reference: Cluster-to-Attraction Fit Matrix

| Segment | LEGOLAND | Alton Towers | Chessington | Warwick Castle | Thorpe Park | SEA LIFE | Madame Tussauds | London Eye | Dungeon | Shrek | Cadbury World |
|---------|----------|--------------|-------------|----------------|-------------|----------|-----------------|------------|---------|-------|---------------|
| 0 Affluent Families | 1.00 | 0.95 | 0.95 | 0.85 | 0.70 | 0.75 | 0.20 | 0.25 | 0.15 | 0.30 | 0.90 |
| 1 Empty Nesters | 0.20 | 0.40 | 0.25 | 0.95 | 0.15 | 0.55 | 0.70 | 0.75 | 0.60 | 0.50 | 0.65 |
| 2 Struggling Families | 0.80 | 0.65 | 0.85 | 0.45 | 0.65 | 0.95 | 0.25 | 0.30 | 0.25 | 0.40 | 0.90 |
| 3 Young Professionals | 0.15 | 0.25 | 0.20 | 0.35 | 0.80 | 0.55 | 0.95 | 1.00 | 0.90 | 0.80 | 0.25 |

Use this matrix to answer "Why is this area recommended for X?" and to validate any attraction-segment alignment logic.
