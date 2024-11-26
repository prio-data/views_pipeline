---
marp: true
title: Spatiotemporal Learning in Action
theme: default #gaia #uncover
class: #invert
math: mathjax
---

# The Violence & Impacts Early-Warning System

**Machine Learning for Anticipatory Action**
&nbsp;

![w:10cm](image_files/VIEWS_logo_tagline.png)
![w:10cm](image_files/UU_PRIO.png)
![bg 100% right:50%](image_files/zstack.png)

---

### The **unreasonable** effectiveness of being prepared:
&nbsp;
**We check the weather forecast**, so we don’t leave the house without an umbrella on a rainy day.
&nb*******sp;
**We check the calendar**, to make sure we don’t double-book ourselves or miss that very important thing.
&nbsp;
**We check traffic before we commute**, to avoid getting stuck in rush hour and get where we need to be on time.

![bg 330% right:33%](image_files/rainy_umbrella.jpg)


---

### In life, preparation saves us from inconvenience. **In violent conflict, preparation could save lives.**

---
**State-based conflicts** remain deadly, with significant loss of life each year.

![bg 95% right:65%](image_files/UCDP_sb_region24.png)

---
**One-sided violence** against civilians continues to take a devastating toll.

![bg 95% right:65%](image_files/UCDP_os_region24.png)

---

**Non-State conflicts** drive increasingly hight counts of fatalities.

![bg 95% right:65%](image_files/UCDP_ns_region24.png)

---
## A global challenge with **no singular solution**

- Conflicts are **highly complex**, crossing borders and involving intricate networks of state and non-state actors.

- The ability of international organizations to prevent or intervene is **increasingly constrained**.

- Individual nations often lack the political will, capacity, or resources to address **conflict or its root causes** alone.

As such, **violent conflict is likely to persist**, inflicting substantial human suffering and hardship for the foreseeable future. Yet..

---

<!---### What if we could **anticipate and prepare** for tomorrow’s conflict?
 ### Anticipating conflict might still help us **save lives and reduce suffering**
--->

### With timely insights, we can shift from reactive responses to **anticipatory actions.**

---

## Turning anticipation into **action**

**Early Warning Systems (EWS)** can provide critical insights, empowering humanitarian actors to respond proactively. 
&nbsp;
- Resource allocation to areas of greatest need.
- Timely deployment of aid workers.
- Civilian evacuation before crises escalate.
&nbsp;

By anticipating conflict, EWS' can **help reduce** human suffering and save lives.

![bg 140% right:33%](image_files/aid.png)

---

### **VIEWS**: developing the next-generation of early warning systems
---

### VIEWS is **More** than an EWS... ![bg 84% right:66%](image_files/circle.png)

But, the focus here will be on the operational EWS.

---

### What the operational VIEWS system **is:**

- A comprehensive (and expanding) collection of **Machine Learning (ML/AI)** models designed for conflict forecasting.

- The models **trained on extensive historical conflict data** to predict future risks with precision.

- A versatile platform enabling robust **research, development, and seamless deployment.**

- Focused on delivering **data-driven insights** to empower humanitarian actors, stakeholders, and policymakers to take **early action**.

---

### What the operational VIEWS system **delivers:**

**Forecasting:** 
- The expected probability of future violent conflict. 
- The expected number of future conflict fatalities.

**Global and local coverage:** 
- Country-level predictions worldwide. 
- Detailed grid-level forecasts for Africa and the Middle East (expanding soon).
- Actor-dyad level forecast coming soon.

**Monthly projections:** 
- Updated monthly
- Providing forecasts for up to 36 months ahead.

![bg 102% right:30%](image_files/two.png)

---

### The **ML** platform

Our platform powers:

**Robust quality assurance** to maintain accuracy and reliability.

**Rigorous model comparison** for continual refinement of predictions.

**Model aggregations** to enhance performance.

![bg 100% right:60%](image_files/pipeline_diagram001.png)

---

### Built for **scalability and transparency**

Our platform adapts to evolving demands with:

- Flexible architecture capable of integrating **new and complex data sources**.

- The ability to incorporate **new cutting-edge models**, ensuring state-of-the-art predictions.

- **Transparent processes to foster trust** in the system and its forecasts.

- A commitment to **continuous improvement**, informed by feedback and advances in technology.

Our mission is to **deliver reliable, actionable insights** through a scalable, transparent, and future-ready system.

---


### Examples of **data sources** used:
:bangbang: **UCDP**: Monthly updated geolocated event data on armed conflicts, including information on actors, locations, and intensity (Current target of our models)

:collision: **ACLED**: Real-time geolocated event data tracking political violence and protests, including conflict events, fatalities, and involved actor

:balance_scale: **DEMSCORE**: A large collection of datasets covering for instance regime types, quality of government, environmental factors, migration and much more

:earth_africa: **WDI**: a database containing information on global development, including economic, social, and environmental indicators

:newspaper: **Factiva**: A comprehensive global news-wire database offering up-to-date insights from reputable sources.

---

### Examples of **ML models** employed:

:robot: **Conventional ML models:** XGBoost and LightGBM uncover patterns in large conventional datasets.

:space_invader: **Bespoke deep learning models:** HydraNet forecasts multiple conflict outcomes using temporospatial data.

:game_die: **Probabilistic models:** Hurdle models handle sparse, zero-inflated data while Hidden Markov Models (HMMs) capture temporal conflict dynamics.

:parrot: **NLP models:** Extract insights from news wire data, with a growing focus on LLMs and RAG systems.



---

### VIEWS as a **complement** to traditional risk analysis

**Systematic and data-driven:** Reduces cognitive bias and ensures consistent analysis.

**Focus on protracted conflicts:** Keeps attention on long-running conflicts that might otherwise fade from focus.

**Spotlighting critical low-risk conflicts:** Identifies seemingly low-risk conflicts with high potential for devastating outcomes.

**Recognizing compound risks:** Detects hidden patterns where interconnected risks amplify conflict.

![bg 130% right:30%](image_files/map_and_compas.png)

---

### What makes **good data** for conflict forecasting?

**Timely:** Data must be consistently maintained and updated frequently - at least monthly - to ensure continuity, capture emerging risks, and respond effectively to rapidly evolving situations.

**Granular:** Sub-national resolution is critical for identifying localized conflict dynamics and hotspots, ensuring targeted and effective interventions.

**Reliable:** Data quality hinges on minimizing non-random missingness, especially temporal or spatial gaps in volatile regions.

**Uncertainty:** Ideally data should include clear estimates of uncertainty - such as confidence intervals or probabilistic ranges and not only a point estimate.

---

### **Challenges** most data sources

**Timeliness gaps:** Many sources are updated annually or semi-annually, failing to keep pace with rapidly changing realities.


**Insufficient granularity:** Many sources lacks sub-national detail, limiting its utility for local conflict forecasting and derived action.

**Measurement biases:** Gaps and distortions - especially in conflict-affected regions - undermine reliability and skew results.

**Incomplete global coverage:** Promising datasets are often regionally limited or exclude key conflict zones.

**Simple point estimates:** Even when data is highly uncertain, point estimates are often provided without clarifying confidence levels, limiting informed decision-making.


---
### **Event data** is currently our most important sources 

This is why conflict event data, such as **UCDP and ACLED**, is currently the strongest data source for our system.

These datasets deliver by far the most predictive power to our models.



---

### What makes a **good model**?

**Precision:** Delivers precise predictions for both conflict probabilities and expected fatalities.

**Scalability:** Easily adapts to expanding datasets, additional regions, and complex conflict dynamics.

**Robustness:** Handles uncertainty, biases, and sparse data while maintaining consistent performance.

**Timeliness:** Generates forecasts efficiently to support real-time or near real-time decision-making.

**Actionability:** Provides outputs that are understandable and directly applicable to practitioner and stakeholder needs.


---

### **Challenges** with many models

**Generalization to unseen data:** Models often struggle to generalize, especially with small sample sizes, zero-inflated data, and static assumptions.

**Handling sparse and skewed data:** Sparse, inconsistent, or zero-inflated spatiotemporal data often requires specialized handling.

**Managing computational costs:** Large spatiotemporal grids and manual preprocessing demand significant resources, limiting scalability.

**Quantifying and communicating uncertainty:** Many models fail to quantify or communicate uncertainty, reducing trust and usability for decision-making.

---

### Levering innovative **solutions**

**In-house models:** Tailored to conflict forecasting challenges like zero-inflated data and spatiotemporal dynamics.

**Evolving designs:** Integrating the latest advancements in machine learning for cutting-edge performance.

**Open to innovation:** Exploring new solutions from the research community to address emerging needs.

This approach ensures our system stays robust, scalable, and effective.

![bg 90% right:45%](image_files/hydranet_PNAS_simple.png)

---

### Tangible **Impact**: VIEWS in the Real World

---

### Engaging with **Policymakers and Practitioners**

**Actively collaborate** with policymakers and practitioners to unlock the potential of **AI-driven conflict forecasting** in real-world operations.

Through commissioned research and proof-of-concepts, we leverage our experience and tools to improving their systems for **decision-making and crisis management**.

![bg 110% right:33%](image_files/GFFO.png)

---

### Supporting Strategic Planning and Risk Modeling

Our forecasts aims to support organizations like **UNHCR, UNESCWA, UNDP, FAO, the German FFO, and the UK FCDO** in strategic planning and risk modeling.

We want to generate insights which organizations like these can rely on to better anticipate conflict risks and **respond more effectively to emerging crises**.

![bg 110% right:33%](image_files/alexa.png)

---

### Partnership with Complex Risk Analytics Fund (CRAF’d)

As a key partner of **CRAF’d**, we contribute to a UN-led multilateral ecosystem that leverages interconnected data to save lives.

CRAF’d prevents duplication of efforts by **fostering collaboration and maximizing the value of technological advancements**.

![bg 110% right:33%](image_files/crafd_thin.png)

---

### Achievements Since 2018

**70+** conflict prediction datasets and **100+** papers/reports advancing conflict forecasting.

Hosted **2 global prediction challenges**, engaging research teams worldwide.

Published a **multilateral flagship report with UNHCR**, demonstrating the transformative potential of leveraging early warning for early action in the Sahel.

Written hundreds of thousands of (mostly well-documented) **open-source lines of code**.

![bg 100% right:33%](image_files/papers.png)

---

### The Future of VIEWS: **Scaling** Our Impact

---

**Expanding Geographic Coverage:** Expand forecasts beyond Africa and the Middle East to cover more conflict-prone regions worldwide, increasing the system’s global applicability.

**Leveraging Newswire Text:** Better integration of newswire data to detect early signals of conflict and provide more timely forecasts of dynamic developements.

**Integrating GIS and Satellite Imagery:** Incorporate GIS data and satellite imagery to enhance geographic precision and track timely changes in conflict zones.

![bg 240% right:40%](image_files/rocket.jpg)

---

**Actor-Based Forecasts:** Introduce actor-specific forecasts to capture how different groups interact and contribute to conflict escalation.

**Dynamic Escalation and De-Escalation Patterns:** Enhance the system’s ability to track how conflicts escalate and de-escalate over time, providing more nuanced insights into conflict dynamics.

**Forecasting Broader Impacts:** Expand forecasting to include related humanitarian crises, such as food insecurity, migration, and public health risks.

<sub>Original image: Johan Spanner</sub>

![bg 240% right:40%](image_files/bodies01.png)

---

**Explicit Modeling of Uncertainty:** Improve the explicit modeling of uncertainty for both input data and forecasts, ensuring more reliable, actionable, and transparent predictions.

**New Decision-Support Algorithms:** Develop algorithms to help organizations allocate resources more effectively, based on evolving conflict risk assessments.

**Developing Scenario-Based Planning Tools:** Offer tools that allow stakeholders to simulate different conflict scenarios and plan responses, improving preparedness.

![bg 150% right:40%](image_files/chaos.png)

---

![bg 100% ](image_files/funders_logos_May2024.png)


---


![bg 110% left:40%](image_files/team2.png)

**Reach out!**

:mailbox: info@viewsforecasting.org
:octopus: https://github.com/views-platform
:globe_with_meridians: https://viewsforecasting.org/
