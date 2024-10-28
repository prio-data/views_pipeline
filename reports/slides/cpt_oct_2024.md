---
marp: true
title: Spatiotemporal Learning in Action
theme: default #gaia #uncover
class: #invert
math: mathjax
---

# **VIEWS:** Violence & Impacts Early-Warning System

**A dive into the Machinery**
&nbsp;

by Simon Polichinel von der Maase
&nbsp;

![w:10cm](image_files/prio_VIEWS.png)
![bg 100% right:50%](image_files/zstack.png)

---

### The **Unreasonable** Effectiveness of Being Prepared

- **I Check the weather forecast**: I don’t leave the house without an umbrella on a rainy day.

- **I Check the calendar**: To make sure I don’t double-book myself or miss that very important thing.

- **I Check traffic before I commute**: to avoid getting stuck in rush hour and get where I need to be on time.

![bg 330% right:33%](image_files/rainy_umbrella.jpg)


---

### Imagine if we could **anticipate** the developement of future conflicts

---



![bg 70%](image_files/UCDP_sb_region24.png)

---

![bg 70%](image_files/UCDP_os_region24.png)

---

![bg 70%](image_files/UCDP_ns_region24.png)

---

### Early Conflict Warning **Matters**

- **Early Warning Systems** (EWS) provide humanitarian actors with critical information and time for **Early Action**.

- They enable **early resource allocation**, personnel deployment, and evacuation of civilians.

- They give stakeholders the tools to anticipate conflict, prepare, and **reduce human suffering**.

![bg 140% right:33%](image_files/aid.png)

---

### What is **VIEWS?**

---

### **More** than the EWS ![bg 70% right:70%](image_files/circle.png)

---

### The **new** platform/pipeline

To integrate new, advanced machine learning models, enabling **reliable** forecasts with real-time updates and **rigorous** model comparisons and aggregations.

![bg 100% right:60%](image_files/pipeline_diagram001.png)

---

### The **aim** of the the platform

To host an advanced **machine learning based** system that delivers **early warnings** of violent conflict by **forecasting** the expected number of future **conflict fatalities** across the globe.

![bg 120% right:50%](image_files/archery.jpg)

---

### The **current** system

**Global and Local Coverage:** It offers forecasts at both the country level and a detailed grid level (Africa and Middle East for now).

**36-Month Forecasts:** New conflict forecasts are updated every month, projecting expected fatalites each month up to 36 months ahead.

**Humanitarian Focus:** The aim is to empower humanitarian organizations and stakeholders to take early action, minimizing human suffering.

![bg 102% right:30%](image_files/two.png)

---

### Examples of **data sources** used in VIEWS:
**UCDP**: Monthly updated geolocated event data on armed conflicts, including information on actors, locations, and intensity (Current target of our models)
&nbsp;
**ACLED**: Real-time geolocated event data tracking political violence and protests, including conflict events, fatalities, and involved actor
&nbsp;
**DEMSCORE**: A large collection of datasets covering for instance regime types, quality of government, environmental factors, migration and much more
&nbsp;
**WDI**: a database containing information on global development, including economic, social, and environmental indicator
&nbsp;

---

### The **current** models

&nbsp;

**Conventional ML Models:** Algorithms like XGBoost and LightGBM combine insights from large datasets and capture complex patterns for conflict prediction.

&nbsp;

**Bespoke Models:** In-house models like HydraNet, a specialized deep learning system, forecast multiple conflict outcomes from complex temporospatial data.

---

![bg 100%](image_files/dashboard01.png)


---

### :space_invader: HydraNet 1.0:

&nbsp;
:brain:  *The deep architecture*
&nbsp;
:space_invader: *The convolutional layers*
&nbsp;
:dart: *The skip connections* 
&nbsp;
:recycle: *The recurrent LSTM structure*


![bg 100% right:50%](image_files/hydranet_PNAS_simple.png)


---
## Analogy:

A **stack of monthly satellite images**, each depicting global conflict fatalities - The stack covers ten years

Examine the stack from the first to the last month

Noisy and complex yet **discernable spatiotemporal patterns** emerge
![bg 100% right:50%](image_files/zstack.png)



---


Including clusters, trends, and sporadicities
&nbsp;
Some patterns generalize **globally**, while others vary by **location**


![bg 100% right:50%](image_files/zstack.png)

---


Can be traced through space and time, enabling qualified predictions of "what-happens-next"
&nbsp;
Less accurate as we forecast further into the future, but they remain far superior to arbitrary guessing

![bg 100% right:50%](image_files/zstack.png)


---


![bg 86%](image_files/timelapse.gif)

---

### VIEWS as a **Complement** to Traditional Risk Analysis

---

**Systematic Approach:** Reduces cognitive bias by using data-driven analysis to keep critical conflicts on the radar.

**Focusing on Protracted Conflicts:** Ensures long-running conflicts don’t fade from attention.

**Spotlighting Low-Risk but Critical Conflicts:** Highlights conflicts that may be at low risk but carry the potential for devastating outcomes.

**Recognizing Compound Risks:** Identifies hidden conflict patterns exacerbated by interconnected, multi-layered risks.

![bg 102% right:30%](image_files/two.png)

---

## Thus the **motivation** for HydraNet was to:

Develop a specialized "machine" capable of processing temporal sequences of images (grids) to **learn intricate spatiotemporal patterns directly from data**.
&nbsp;
It should prioritize **generalization across time and space** while retaining **specific historical information** for each grid-cell.
&nbsp;
The "machine" should be able to generate qualified estimates for **cell-wise patterns in future, unobserved spatial grids**
&nbsp;
**HydraNet** is a bespoke (custom) ML model designed specifically to excel at these tasks


---

### Tangible **Impact**: VIEWS in the Real World

---

### Engaging with Policymakers and Practitioners

**Actively collaborate** with policymakers and practitioners to unlock the potential of **AI-driven conflict forecasting** in real-world operations.

Through commissioned research and proof-of-concepts, we leverage our experience and tools to improving their systems for **decision-making and crisis management**.

![bg 110% right:33%](image_files/GFFO.png)

---

### Supporting Strategic Planning and Risk Modeling

Our forecasts supports organizations like **UNHCR, UNESCWA, UNDP, FAO, the German FFO, and the UK FCDO** in strategic planning and risk modeling.

These organizations rely on our forecasts to better anticipate conflict risks and **respond more effectively to emerging crises**.

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


![bg 240% left:42%](image_files/team.png)

Thanks for listening!

:bust_in_silhouette: Simon Polichinel von der Maase
:world_map: PRIO, Oslo, Norway
:mailbox: simmaa@prio.org
:octopus: https://github.com/prio-data/views_pipeline
:globe_with_meridians: https://viewsforecasting.org/
