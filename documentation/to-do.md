# Ex-ante Hackathon:

+ [x] Deployment Strategy
   - Result: Decided on local server-side deployment.

+ [x] Pipeline Structure
   - Result: Initial pipeline structure finalized and documented on Simon's whiteboard... (digital to come)

+ [x] Orchestration/Flow Tool
   - Result: Prefect chosen as the orchestration tool; https://www.prefect.io/.

+ [x] Tracking/Monitoring Tool
   - Result: W&B selected for tracking/monitoring; https://wandb.ai/.

+ [v] Repository Structure
   - Draft for the repository structure on Notion: https://www.notion.so/model_repo_structure-draft-3bd28dd2605a41fab02bd020a4edbe13

+ [v] Model Metadata
   - Draft for the model metadata content on Notion: https://www.notion.so/model_metadata-python-dict-draft-example-work-in-progress-451d0a66c4f1456b83df9bfef79ffa62

+ [v] Naming Convention
    - Model Naming result: adjective_noun_ddmmyyyy, e.g., pink_panther_24122024.
    - Essential scripts draft: https://www.notion.so/model_repo_structure-draft-3bd28dd2605a41fab02bd020a4edbe13
    - Essential artifacts draft: https://www.notion.so/model_repo_structure-draft-3bd28dd2605a41fab02bd020a4edbe13
    
+ [v] Model Definitions
   - Draft clarifying the definition of models on Notion: [Notion link]

+ [ ] Input/Output Standardization
   - Draft on the agreed standard for input and output formats: [Notion link]

+ [v] Decide on initial relevant metrics to log on W&B
	- MSE, LMSE, Jeffreys Divergence, Jenson-Shannon Divergence, more? 

+ [ ] Miniconda Environment on Fimbulthul

+ [ ] Settle on a general folder structure on Fimbulthul (beyond model repo)

+ [ ] Develop a fully executable reference model on Fimbulthul, adhering to the new repository structure (Simon's task).

+ [ ] Consider and document CI/CD practices for structure, and naming. and definition adherence.

# Intra Hackathon:

- [ ] Fully implement two baseline models executable on Fimbulthul adhering to all conventions decided ex-ante Hackathon 
- [ ] Fully implement two simple but diverse models from the current production pipeline. Must be executable on Fimbulthul adhering to all conventions decided ex-ante Hackathon
- [ ] Fully implement one bespoke model such as HydraNet or Hurdle Regression. Must be executable on Fimbulthul adhering to all conventions decided ex-ante hackathon 
- [ ] Fully implement two place-holder/baseline ensembles (mean and median). Must be executable on Fimbulthul adhering to all conventions decided ex-ante hackathon 
- [ ] Implement alert gate for input drift - summary logged on W&B 
- [ ] Implement alert gate for output drift - summary logged on W&B 
- [ ] All predictions (output) must be visualized as maps on W&B.  
- [ ] At each month t, all past predictions made about month t (at t-1, t-2 ... t-36) must be evaluated (online evaluation and check for performance drift alert gate).
- [ ] All elevation metrics (decided on ex anta hackathon) must be logged and visualized (including as maps) on W&B (online evaluation and check for performance drift alert gate)
- [ ] A full run, from fetching query set to allocation predictions in the prediction store, for all models and ensembles must be executable through Prefect. 


# Ex-post Hackathon:
- [ ] **Debriefing:**  
	- Assess if initial deliverables have been achieved.
	- Review technical aspects of the hackathon
	- Assess documentation quality and completeness
	- Reflect on team collaboration and dynamics
	- Discuss follow-up actions and future improvements


:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# PROGRAM Intra Hackathon

**Day 0: Monday (Arrival)**

- [ ] Simon ensures the reference model runs from the cabin on Fimbulthul with some outputs to W&B.
- [ ] Altogether, review the deliverables and the program
- [ ] Simon and Sara loot nearby town for food, drinks, and snack.
- [ ] Noorain will start to implement the zero and no-change baseline models in the new repo structure. Tentative implementations or placeholders for W&B + Prefect specific code in all scripts
- [ ] Xiaolong will start to implement two diverse production models in the new repo structure. Tentative implementations or placeholders for W&B + Prefect specific code in all scripts
- [ ] Mihai & Jim start on input drift detection (alert gate) with logging on W&B.
- [ ] Malika & Sara do initial tests on getting metrics and visualizations (maps) to W&B.

**Day 1: Tuesday**

- [ ] Malika and Sara design final logging and visualizing scheme for online evaluation on W&B  
- [ ] Noorain finalizes implementing the zero and no-change baseline models in the new repo structure. Start conform code such that it adheres to the W&B scheme design bu m/s. 
- [ ] Xiaolong finalizes implementing the two diverse production models in the new repo structure. Start conform code such that it adheres to the W&B scheme design bu m/s. 
- [ ] Mihai & Jim finalize input drift detection (alert gate) with logging on W&B. Possible starting on output drift detection (alert gate) with logging on W&B.
- [ ] Simon fully implements a bespoke model in the new repo structure. Tentative implementations or placeholders for W&B + Prefect specific code in all scripts.

**Day 2: Wednesday**

- [ ] Noorain creates a simple ensemble (mean for "production"). Outputs and eval metrics should be ready to be logged and visualized on W&B.
- [ ] Xiaolong creates a simple ensemble (median for "shadow"). Outputs and eval metrics should be ready to be logged and visualized on W&B.
- [ ] Mihai & Jim implement output drift detection (alert gates) with logging on W&B.
- [ ] Malika focuses on correct and robust implementation of the online evaluation.
- [ ] Sara writes documentation paper.
- [ ] Simon starts testing the Prefect flow routine.

**Day 3: Thursday**

- [ ] Mihai & Jim finalize output drift detection (alert gates) with logging on W&B.
- [ ] Malika, Mihai, and Jim review and finalize the online evaluation and performance alert gate
- [ ] Simon, Noorain, and Xiaolong implement full Prefect flow across all models and ensembles.
- [ ] Sara finishes the documentation paper and takes notes and reports for the debriefing

**Day 4: Friday (Departure)**

- [ ] Clean the cabin.
- [ ] Go to Oslo.
- [ ] Dinner and drinks.
