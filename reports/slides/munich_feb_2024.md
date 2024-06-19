---
marp: true
title: Test
theme: default #gaia #uncover
class: #invert
math: mathjax
---

![bg 90% right](zstack1.png)

# HydraNet 1.0/1.5 
**Spatiotemporal Learning Unleashed**

&nbsp;
&nbsp;
Simon P. von der Maase
&nbsp;

![w:10cm](prio_VIEWS.png)

---

## What?

We (VIEWS) are concerned with **Early Warning**
&nbsp;
The explicit aim is the facilitate **early action** -  i.e. to **inform critical decisions** and guide the efficient and **timely allocation** of scarce resources and relevant personnel
&nbsp;
To this end, we must provide stakeholders, decision-makers, and practitioners with **information beyond the expected level of future violence** (conventional conflict forecasting)
&nbsp;
This includes **information on expected impacts**: Food insecurities, access to water, migration, health risks, gendered security issues etc.

---

## HydraNet:

- A **Deep** Neural Network :brain:
- Using **convolutional** layers and **skip connections** (a U-Net) :space_invader:/:dart:
- Structured in a **recurrent** manner (Long Short Term Memory) :recycle:
- Capable of **automatically** learning and extrapolating (forecasting) spatiotemporal patterns :chart_with_upwards_trend:
- For instance, useful for predicting violent conflict, or related phenomena, at a **highly disaggregated** temporal and spatial granularity (such as pgm) :globe_with_meridians:

&nbsp;

*Admittable a lot of jargon and not super helpful without some background and context - so let's rewind a bit*

---

## VIEWS: The Violence and Impact Early Warning System:

A **machine learning** system producing forecasts of violent conflict
&nbsp;
New updated 36-months-ahead forecast **every month**

![bg 115% right](prio_grid.png)

---

At country (global coverage) and **PRIO grid** (Africa and ME coverage) level
&nbsp;

The PRIO grid (pg) is a **spatial grid** with square grid cells of $0.5 \times 0.5$ decimal degree  
&nbsp;

Approximately $55km \times 55km$ at the equator.
&nbsp;

**HydraNet** generates forecast on the pgm level

![bg 115% left](prio_grid.png)

---



## When I say Machine Learning (ML) I mean:

A subset of artificial intelligence
&nbsp;

Through a combination of computer algorithms and statistical tools, we allow computers to learn patterns directly from our data 
&nbsp;
I.e. we are not explicitly programming hard rules

---

## Example: 

Creating a chess program by writing explicit code such as "if black queen at E5 ..."
&nbsp;
Versus allowing an ML model to look at 10.000.000 million chess games and let it figure out the best rules itself

![bg 170% right](chess.jpg)

---

## Example: 

If you know chess, you can imagine how overwhelming the first approach would be
&nbsp;
And naturally, large-scale conflict is vastly more complex than chess

![bg 170% left](chess.jpg)

---

## ML, a driving force behind:

:speech_balloon: Natural language processing and machine translation
&nbsp;
:mag_right: Image recognition and computer vision
&nbsp;
:robot: Autonomous vehicles and robotics
&nbsp;
(Image: Johan Spanner)
&nbsp;
![bg 190% right](img0.png)

---

## Examples of data sources used in VIEWS:
**UCDP**: Monthly updated geolocated event data on armed conflicts, including information on actors, locations, and intensity (Current target of our models)
&nbsp;
**ACLED**: Real-time geolocated event data tracking political violence and protests, including conflict events, fatalities, and involved actor
&nbsp;
**DEMSCORE**: A large collection of datasets covering for instance regime types, quality of government, environmental factors, migration and much more
&nbsp;
**WDI**: a database containing information on global development, including economic, social, and environmental indicator
&nbsp;

---

## We are currently relying on:

**General-purpose** supervised ML algorithms such as XGboost and LightGBM  
&nbsp;
These are powerful algorithms working on conventional **row/column data frames** - spreadsheets if you will
&nbsp;
**Not inherently designed** to take account of spatiotemporal patterns
&nbsp;
An issue since, we would expect a given observation (pg) to be influenced by what happens in **adjacent cells**, both through time and space

---

## Why?

Self-reinforcing feedback loops of violence 
&nbsp;
- Military socialization,
- Militarization of local authorities, 
- Increasingly influential militaries, 
- Fragmented political economies, 
- Social network disintegration, 

![bg 140% right](patches.png)

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

![bg 140% left](patches.png)

---
## Currently deployed solution:

The simple solution is to manually create **a lot** of transformed features 
&nbsp;
For instance **temporal and spatial lags** (e.g. conflict magnitude in spatially or temporally adjacent cells)
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


![bg 110% right](zstack02.png)

---
## Analogy 2:

A **stack of monthly satellite images**, each depicting global conflict fatalities - The stack covers ten years

Examine the stack from the first to the last month

Noisy and complex yet **discernable spatiotemporal patterns** emerge
![bg 110% left](zstack02.png)


---

## Analogy 2 (contiued):

Including clusters, trends, and sporadicities
&nbsp;
Some patterns generalize **globally**, while others vary by **location**


![bg 110% right](zstack02.png)

---

## Analogy 2 (contiued):


Can be traced through space and time, enabling qualified predictions of "what-happens-next"
&nbsp;
Less accurate as we forecast further into the future, but they remain far superior to arbitrary guessing

![bg 110% left](zstack02.png)

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


![bg 90% right](hydranet_PNAS_simple.png)

---

[timelapse](./timelapse.mp4)

![bg 60% ](trio_00.png)

---


## From 1.0 to 1.5

Back to the fact that the point of **Early Warning** is **Early Action** 
&nbsp;
E.g. **Early allocation** of resources and personnel
&nbsp;
For effective allocation, stakeholders, policymakers, and practitioners need more information than "simply" the kind and magnitude of expected violence 
&nbsp;
They **need information on the expected impact**: Food insecurities, access to water, migration, health risks, gendered security issues etc. 

---

## To what extent can HydraNet help?

Again: HydraNet's strength comes from its capacity to effectively and automatically learn salient and highly complex spatiotemporal patterns
&nbsp;
**If a phenomenon can be expected to exhibit temporal and spatial dependencies - i.e. if distances matter - then HydraNet is a reasonable candidate**
&nbsp;
Several of the conflict-induced impacts we are interested in can indeed be expected to exhibit some amount of spatiotemporal dependencies  

---

To the extent that we can muster the computational power, HydraNet can forecast an arbitrary number of spatiotemporal phenomena
&nbsp;
However, there is probably no need to forecast everything at once...
&nbsp;
Dedicated solutions can easily be implemented for specific rosters of phenomena of interest


![bg 130% right](space_invader.jpg)

---

Hopefully, HydraNet - or at least the ideas and components behind it - can find use outside the VIEWS consortium 

---

![bg 50% left](simon.png)


# Questions?

Thanks for listening! 

:bust_in_silhouette: Simon Polichinel von der Maase
:globe_with_meridians: PRIO, Oslo, Norway
:mailbox: simmaa@prio.org
:octopus: https://github.com/Polichinel/

&nbsp;
