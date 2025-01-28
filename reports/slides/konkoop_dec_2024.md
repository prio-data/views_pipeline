---
marp: true
title: Konkoop_workshop
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

# Introduction.

---

## About me:

:bust_in_silhouette: **Simon Polichinel von der Maase**
:globe_with_meridians: **PRIO, Oslo, Norway**
&nbsp;
:briefcase: **Senior Researcher:** At the Peace Research Institute Oslo (PRIO), working on conflict forecasting and AI for peace research.
&nbsp;
:technologist: **Head of Model Development & Deployment:** Leading the MD&D team at VIEWS to our deployed conflict forecasting systems.
&nbsp;


![bg 100% left:30%](image_files/simon.png)


---
##  Current focus areas:

:space_invader: **HydraNet**: Bespoke deep learning architecture (U-Net + LSTM) for forecasting temporospatial (conflict) patterns.

:gear: **The new VIEWS ML platform**: Creating a robust and transparent conflict forecasting platform.  

:rotating_light: **Conflict Return Periods**: Estimating the recurrence of high-impact conflict events to support risk assessment and preparedness 

:busts_in_silhouette: **Actor-Level Dynamics**: Using LLMs and newswire text to study conflict escalation patterns between organized actors.  

![bg 70% left:30%](image_files/my_qr.png)


---
##  Current agendas:

:link: **Bridging the Gap:** Connecting model outputs to strategic decisions and early actions.

:hammer_and_wrench: **Specialized Models:** Promoting the development and adoption of tailored models for better forecasting of temporospatial patterns.

:handshake: **Fostering Collaboration:** Encouraging cumulative efforts and collaborations to avoid duplication of efforts and subpar products.

:shield: **Robust MLOps:** Emphasizing the critical role of MLOps, DevOps, and QA in ensuring trust, transparency, and reliability in AI/data-driven social science applications.

![bg 75% left:30%](image_files/unidir.png)

---


# Why.

---

### The **unreasonable** effectiveness of being prepared:
&nbsp;
**We check the weather forecast**, so we don’t leave the house without an umbrella on a rainy day.
&nbsp;
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

As such, **violent conflict is likely to persist**, inflicting substantial human suffering and hardship for the foreseeable future.

---


### However, with timely insights, we can shift from reactive responses to **anticipatory actions.**

---

## Turning anticipation into **action**

**Early Warning Systems (EWS)** can provide critical insights, empowering humanitarian actors to respond proactively. 
&nbsp;
- Resource allocation to areas of greatest need.
- Timely deployment of aid workers.
- Civilian evacuation before crises escalate.
&nbsp;

By anticipating conflict and derived impacts, EWS' can **help reduce** human suffering and save lives.

![bg 140% right:33%](image_files/aid.png)

---

## VIEWS: A **complement** to traditional risk analysis I

:computer: **Data-driven analysis:** Provides consistent, data-driven insights, reducing human cognitive bias and ensuring reproducibility across regions and time.

:calendar: **Strategic prioritization of overlooked conflicts:** Consistent focus on long-term and low-priority conflicts.

:world_map: **Granular temporospatial insights:** Produce high-resolution forecasts, pinpointing localized risks.

![bg 130% right:30%](image_files/map_and_compas.png)

---

## VIEWS: A **complement** to traditional risk analysis II

:jigsaw: **Uncovering complex, opaque risks:** Detecting non-linear patterns, interconnected risks, and compound dynamics.

:zap: **Real-Time Monitoring and Adaptability:** continuously updates forecasts in real time, reflecting rapidly changing conflict dynamics.

:handshake: **Scalable Support for Decision-Making:** Frees up human resources by processing vast amounts of data, enabling experts to focus on nuanced, strategic decisions.

![bg 130% left:30%](image_files/map_and_compas.png)

---

### **Analogy:** Experts and AI Systems

Imagine you’re trying to navigate through a new city. 

You have **two options**:

1. Ask a **seasoned taxi** driver for directions.  
2. Use **Google Maps** to guide you.  

Both approaches have strengths and limitations. 

**Right?**

![bg 110% right:40%](image_files/arm_wrestling.png)

--- 

### The Seasoned Taxi Driver: **Deep, Local Expertise**

- **Deep, local knowledge**: Hidden shortcuts, traffic quirks, and neighborhood patterns.  
- **Contextual understanding**: Knows unspoken rules, cultural nuances, and local behaviors.  
- **Intuition**: Years of experience make them adaptable to unexpected situations.  

But their expertise is **limited** - they're ill equipped to guide you in a different city or scale their insights globally.  

![bg 110% right:40%](image_files/taxi.png)

---

### Google Maps: **Global, Scalable, and Systematic**

- **Global reach**: Works anywhere, from local streets to global cities.  
- **Real-time updates**: Tracks traffic, closures, and conditions to provide accurate directions.  
- **Scalability**: Processes millions of routes simultaneously, relatively uniformly,  and with on fatigue.  

But it struggles to incorporate **idiosyncratic, qualitative local knowledge** - like the hills in Oslo or the very creative road infrastructure solutions leading in to the city. 

![bg 100% right:40%](image_files/google_maps.png)

---

### Together, they could **bridge these gaps**.  

The **taxi driver’s expertise** adds depth, intuition, and qualitative understanding.  

While **Google Maps’ data** adds scalability, reliability, and consistency.  

The best of both of worlds.


![bg 200% right:40%](image_files/evangelion.jpg)


---

## VIEWS + Human Experts: A Winning Combination  

Similarly, (in theory) EWS' such as VIEWS and human experts should form powerful partnerships, combining their unique strengths:

:raising_hand_woman: **Human Experts**  
   - Bring deep contextual understanding of conflict dynamics.  
   - Interpret cultural nuances, political motives, and qualitative insights.  

:robot: **VIEWS**  
   - Scales insights globally, monitoring conflicts across regions.  
   - Detects hidden risks and compound patterns.  
   - Provides real-time updates, adapting quickly to changing dynamics.  

---
  
## Questions, comments, curiosities so far? 



---

### Let’s take a moment for some early **reflections** together:  

**What do you think/see as the biggest challenge in forecasting conflict?** Is it gathering data, understanding trends, or predicting outcomes?  
&nbsp;
**What obstacles do you see in regards to using conflict forecasting to make decisions?** Is it access to data, trust in models, or something else?  
&nbsp;
**If you had a tool like VIEWS, what would you want it to deliver?** Forecasts, alerts, localized insights, or?

&nbsp;

![bg 200% left:30%](image_files/thinker.jpg)

---

# What.

---

### VIEWS is **More** than an EWS. ![bg 84% right:66%](image_files/circle.png)

But, the main focus here will be on the operational EWS.

---

### **What this mission is:** developing, testing, and deploying the next-generation of early warning systems.

---

### What the operational VIEWS system **is:**

- A comprehensive (and expanding) collection of **Machine Learning (ML/AI)** models forecasting conflict.

- The models **trained on extensive historical data** to predict future risks with precision.

- A versatile platform enabling robust **research, development, and seamless deployment.**

- Focused on delivering **data-driven insights** to empower humanitarian actors, stakeholders, and policymakers to take **early action**.

---



### When I say Machine Learning (ML) I mean:

A subset of artificial intelligence (**AI**)
&nbsp;

Through a combination of computer algorithms and statistical tools, we allow computers to **learn patterns directly from our data** 
&nbsp;
I.e. we are **not explicitly programming hard rules**

---

### Example: 

Creating a chess program by writing explicit code such as "if black queen at E5 ..."
&nbsp;
Versus allowing an ML model to look at 10.000.000 million chess games and let it figure out the best rules itself

![bg 170% right](image_files/chess.jpg)

---

### Example: 

If you know chess, you can imagine how overwhelming the first approach would be
&nbsp;
And naturally, large-scale conflict is vastly more complex than chess

![bg 170% left](image_files/chess.jpg)


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

![bg 86%](image_files/timelapse.gif)

---

### Our **ML** platform

**Robust quality assurance** to maintain precision and reliability.

**Rigorous model comparison** for continual performance improvement.

**Model aggregations** to enhance performance and stability.

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

### :link: The [views-platform](https://github.com/views-platform) on GitHub

---

### Examples of **data sources** used:
:bangbang: **[UCDP](https://ucdp.uu.se/)**: Monthly updated geolocated event data on armed conflicts, including information on actors, locations, and intensity (Current target of our models)

:collision: **[ACLED](https://acleddata.com/)**: Real-time geolocated event data tracking political violence and protests, including conflict events, fatalities, and involved actor

:balance_scale: **[DEMSCORE](https://www.demscore.se/)**: A large collection of datasets covering for instance regime types, quality of government, environmental factors, migration and much more

:earth_africa: **[WDI](https://databank.worldbank.org/reports.aspx?source=2&country=ARE)**: a database containing information on global development, including economic, social, and environmental indicators

:newspaper: **[Factiva](https://www.dowjones.com/professional/factiva/)**: A comprehensive global news-wire database offering up-to-date insights from reputable sources.

---

### Examples of **ML models** employed:

:robot: **Conventional ML models:** XGBoost and LightGBM uncover patterns in large conventional datasets.

:space_invader: **Bespoke deep learning models:** HydraNet forecasts multiple conflict outcomes using temporospatial data.

:game_die: **Probabilistic models:** Hurdle models handle sparse, zero-inflated data while Hidden Markov Models (HMMs) capture temporal conflict dynamics.

:parrot: **NLP models:** Extract insights from news wire data, with a growing focus on LLMs and RAG systems.



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

![bg 100% right:40%](image_files/ucdp.png)

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

---

## Questions, comments, curiosities so far? 

---


### Example of bespoke in-house model: **HydraNet**

---

## BAck to the importance of event data

Theories of self-reinforcing feedback loops of violence 
- Military socialization,
- Militarization of local authorities, 
- Increasingly influential militaries, 
- Fragmented political economies, 
- Social network disintegration, 

![bg 200% right:30%](image_files/patches.png)

---

## Why? (continued) 

- Polarization of social identities, 
- Challenges related to reintegrating veterans, 
- Firearm circulation,
- inter-group grievances, 
- Destruction of infrastructure, 
- Incurred debt, 
- Disrupted trade, 
- Impeded growth, 
- reduce state capacity, 
- etc...

![bg 200% left:30%](image_files/patches.png)

---
## Currently deployed solution:

The simple solution is to manually create **a lot** of transformed features 
&nbsp;
For instance **temporal and spatial lags** (e.g. conflict magnitude in spatially or temporally adjacent grid cells)
&nbsp;
And decay functions measuring **time since the last conflict**, last peace etc 
&nbsp;
Note, that these features have historically been constructed to capture theoretically grounded phenomena such as **conflict traps and conflict diffusion**

---
## However: 

We do not actually know the underlying functional form for conflict traps or conflict diffusion - they are in essence the product of legions of different very complex sub-phenomena
&nbsp;

And even if we did know the approximate functional form, there is no guarantee that the predictive power of past conflict patterns arises solely from phenomenons such as traps and diffusion

---
## That is:

Data on conflict patterns (UCDP) is the most granular and most frequently updated data used, it ends up serving as a **high variance predictive proxy** for a host of other potentially unobserved or poorly measured factors
&nbsp;

In other words, the data on past conflict patterns is a **sponge soaked in signals** from everything that happens in conflict (also why past patterns are our best predictors)
&nbsp;

Thus, it is likely **unfeasible to harness the full predictive potential** of past patterns using conventional manual feature engineering

---

## In sum:

:sweat: Manual feature engineering is a major resource drain and a hassle. Predicting an increasing number of outcomes exacerbates this issue exponentially
&nbsp;
:monocle_face: And, no matter the resources put into manual feature engineering, we are unlikely to effectively capture the predictive patterns we are looking for  
&nbsp;
:thinking: We need a framework that is specifically designed to learn spatiotemporal patterns automatically from the data

---

## :space_invader: HydraNet 1.0:
Is a solution to this issue. I will not get technical regarding the specificities here, but keep to a high level of intuition. The main components are:
&nbsp;
:brain:  *The deep architecture*
&nbsp;
:space_invader: *The convolutional layers*
&nbsp;
:dart: *The skip connections* 
&nbsp;
:recycle: *The recurrent LSTM structure*

---
## Analogy 1:

Imagine predicting the next frame in a movie. You could consider:

- the current frame 

- The last couple of frames

- And the plot's general progression.

Probably a manageable task  


![bg 110% right](image_files/zstack.png)

---
## Analogy 2:

A **stack of monthly satellite images**, each depicting global conflict fatalities - The stack covers ten years

Examine the stack from the first to the last month

Noisy and complex yet **discernable spatiotemporal patterns** emerge
![bg 110% left](image_files/zstack.png)


---

## Analogy 2 (contiued):

Including clusters, trends, and sporadicities
&nbsp;
Some patterns generalize **globally**, while others vary by **location**


![bg 110% right](image_files/zstack.png)

---

## Analogy 2 (contiued):


Can be traced through space and time, enabling qualified predictions of "what-happens-next"
&nbsp;
Less accurate as we forecast further into the future, but they remain far superior to arbitrary guessing

![bg 110% left](image_files/zstack.png)

---


## Thus the motivation for HydraNet was to:

Develop a specialized "machine" capable of processing temporal sequences of images (grids) to **learn intricate spatiotemporal patterns directly from data**.
&nbsp;
It should prioritize **generalization across time and space** while retaining **specific historical information** for each grid-cell.
&nbsp;
The "machine" should be able to generate qualified estimates for **cell-wise patterns in future, unobserved spatial grids**
&nbsp;
**HydraNet** is a bespoke (custom) ML model designed specifically to excel at these tasks

---

## Quick note:

In theory, any adequately deep neural network would be able to do this if we had infinite data and computing power.

But only one history of violence - and only 30-ish years of data

And compute power is always scares

The relative strength of HydraNet is its ability to automatically and effectively learn highly complex spatiotemporal patterns given very limited data

---


## Why "Hydra"?
- Can forecast multiple outputs simultaneously
&nbsp;
- Currently forecasts 3 different types of violence (**state-based**, **one-side**, **non-state-based**)
&nbsp;
- Both probabilities (classification) and magnitudes (regression) of expected conflict fatalities


![bg 90% right](image_files/hydranet_PNAS_simple.png)

---

## Questions, comments, curiosities so far? 

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

## Questions, comments, curiosities so far? 

---

![bg 110% left:40%](image_files/team2.png)

**Reach out!**

:mailbox: info@viewsforecasting.org
:octopus: https://github.com/views-platform
:globe_with_meridians: https://viewsforecasting.org/
