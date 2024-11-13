---
marp: true
title: Spatiotemporal Learning in Action
theme: default #gaia #uncover
class: #invert
math: mathjax
---

# **VIEWS:** Violence & Impacts Early-Warning System

**Machine Learning for Anticipatory Action**
&nbsp;

Simon Polichinel von der Maase
&nbsp;

![w:10cm](image_files/prio_VIEWS.png)
![bg 100% right:50%](image_files/zstack.png)

---

### The **unreasonable** effectiveness of being prepared
&nbsp;
**I check the weather forecast**: So I don’t leave the house without an umbrella on a rainy day.
&nbsp;
**I check the calendar**: To make sure I don’t double-book myself or miss that very important thing.
&nbsp;
**I check traffic before I commute**: To avoid getting stuck in rush hour and get where I need to be on time.

![bg 330% right:33%](image_files/rainy_umbrella.jpg)


---

### Imagine if we could **anticipate** the developement of future conflicts

---


### Early conflict warning **matters**
&nbsp;
- **Early Warning Systems** (EWS) provide humanitarian actors with critical information and time for **Early Action**.
&nbsp;
- They enable **early resource allocation**, personnel deployment, and evacuation of civilians.
&nbsp;
- They give stakeholders the tools to anticipate conflict, prepare, and **reduce human suffering**.

![bg 140% right:33%](image_files/aid.png)

---

### What is **VIEWS?**

---

### **More** than an EWS ![bg 84% right:66%](image_files/circle.png)

---

### The **Machine Learning** platform

A system of advanced machine learning models, enabling **reliable** forecasts with near monthly updates and **rigorous** model comparisons and **aggregations**.

![bg 100% right:60%](image_files/pipeline_diagram001.png)

---


### The **forecasts** in a nutshell

**Forecasting:** The probability of violence and the expected number of future conflict fatalities.

**Global and Local Coverage:** Both the country level (global) and a detailed grid level (Africa and Middle East for now).

**36-Month Forecasts:** New conflict forecasts are updated every month, projecting each month, 36 months ahead.

**Humanitarian Focus:** The aim is to empower humanitarian organizations and stakeholders to take early action, minimizing human suffering.

![bg 102% right:30%](image_files/two.png)

---

### VIEWS as a **complement** to traditional risk analysis

**Systematic Approach:**  Data-driven approach to reduces human cognitive bias.

**Focusing on Protracted Conflicts:** Ensures long-running conflicts don’t fade from attention.

**Spotlighting Low-Risk but Critical Conflicts:** Highlights conflicts that may be at low risk but carry the potential for devastating outcomes.

**Recognizing Compound Risks:** Identifies hidden conflict patterns exacerbated by interconnected risks.

![bg 130% right:30%](image_files/map_and_compas.png)

---


### Examples of **data sources** used in VIEWS' ML platform:
:bangbang: **UCDP**: Monthly updated geolocated event data on armed conflicts, including information on actors, locations, and intensity (Current target of our models)

:collision: **ACLED**: Real-time geolocated event data tracking political violence and protests, including conflict events, fatalities, and involved actor

:balance_scale: **DEMSCORE**: A large collection of datasets covering for instance regime types, quality of government, environmental factors, migration and much more

:earth_africa: **WDI**: a database containing information on global development, including economic, social, and environmental indicators

:newspaper: **Factiva**: A comprehensive global news-wire database offering up-to-date insights from reputable sources.

---

### Why **Arms and Ammunition Flow** data isn’t currently used in VIEWS...

---

### While arms flow data could theoretically provide relevant signals, **practical limitations** prevent its use.
&nbsp;
**Timeliness**: Most sources are updated annually or semi-annually, unsuitable for near real-time forecasting.
&nbsp;
**Granularity**: Datasets are often aggregated and lack details on sub-national distributions and end-users.
&nbsp;
> If I have overlooked a brilliant data source here, please let me know.

![bg 130% right:40%](image_files/uncertainty_sign.png)


---

**Measurement error and reporting biases**: Much data is self-reported or voluntary, leading to gaps and biases, especially in politically sensitive areas and in tracking illicit arms trade.
&nbsp;
**Global Coverage Gaps**: Several otherwise promising data sources cover only select countries.
&nbsp;
**Narrow Focus**: Some sources provide detailed data on illicit arms in specific conflicts but are hard to scale or standardize for broad coverage.

![bg 130% right:40%](image_files/uncertainty_sign.png)


---

### **To summarize**, for arms flow data to be useful in EWS, it should ideally:

- **Provide Near Real-Time Updates**: Timely data is essential for anticipating and responding to emerging conflict risks.

- **Offer Greater Granularity**: Data should include sub-national distributions and details on end-users.

- **Enhance Reporting Reliability**: Reduce biases by standardizing reporting practices and minimizing reliance on self-reported data.

- **Expand Global Coverage**: Broaden the coverage to encompass more (ideally all) countries.

- **Report Measurement of Data Uncertainty**: Provide transparency on data reliability, including estimates of reporting biases and measurement errors.

---

### Achieving this **vision** requires:

- **Robust Technical Infrastructure**: A reliable and scalable platform to collect, process, and analyze arms flow data in near real-time.

- **Deep Domain Knowledge**: Expertise in arms trade, conflict dynamics, and data science working together to collect and leverage the data effectively.

- **Consistent and Sustainable Funding**: Ongoing financial support to ensure data collection, platform maintenance, and development.

- **Long-Term Commitment from Funders**: A stable, long-term investment is critical for building a reliable arms flow data and ensure incorporation in EWS.

- **Collaborative Global Partnerships**: International collaboration to ensure data coverage, especially in underrepresented regions.

---

### Hopefully, this conference is the **first step** towards realizing this vision

---


![bg 110% left:50%](image_files/team2.png)

**Thanks for listening!**

:bust_in_silhouette: Simon Polichinel von der Maase
:world_map: PRIO, Oslo, Norway
:mailbox: simmaa@prio.org
:octopus: https://github.com/prio-data/views_pipeline
:globe_with_meridians: https://viewsforecasting.org/
