# **MVP Pipeline (Target: Start of November)**

## **Primary Goal**  
The new pipeline should generate predictions that are consistent with the old pipeline’s performance while incorporating HydraNet PGM-level predictions. Although some model implementations will differ, the overall predictive performance is expected to be as good as, or better than, the old pipeline.

---

## **MVP Requirements and Deliverables**

### **1. PGM Predictions from Legacy Models**  
Produce PGM-level predictions from the majority of models implemented in the old pipeline. The models to be included should be referenced from the model [catalogs](https://github.com/prio-data/views_pipeline/tree/main/documentation/catalogs), which track the transition to the new pipeline. Where applicable, unmodified DARTS models should be considered if their classification performance meets the project’s needs. Adaptation efforts for any individual model should not exceed three working days. Any models that cannot be adapted within this timeframe should be deprioritized for now. Unmaintainable or deprecated models will not be included in the MVP.

### **2. HydraNet PGM Predictions**  
Integrate and deploy HydraNet models to produce PGM-level predictions. At least one HydraNet model must be fully operational and producing predictions within the system, ensuring its compatibility alongside legacy models.

### **3. CM Predictions from Legacy Models**  
Produce CM-level predictions from the majority of models implemented in the old pipeline. The models to be included should be referenced from the model [catalogs](https://github.com/prio-data/views_pipeline/tree/main/documentation/catalogs), which track the transition to the new pipeline. Where applicable, unmodified DARTS models should be considered if their classification performance meets the project’s needs. Complex adaptations for CM models should be deprioritized unless they are critical for ensuring overall system functionality and performance.

### **4. Ensembles**  
Implement a mean ensemble method for aggregating predictions from both PGM and CM-level models. Additionally, deploy a median ensemble as a shadow model to serve as a baseline for comparison and validation purposes.

### **5. Calibration (Temporary Solution)**  
Utilize Jim’s existing calibration script to temporarily align ensemble predictions at the PGM and CM levels. While this solution will suffice for the MVP, developing a more robust and accurate calibration method will be a top priority post-MVP as Jim has marked the current solution as "hacky as hell".

### **6. Prefect Orchestration**  
Implement Prefect orchestration to manage the entire pipeline, focusing on data fetching, model training, and forecast generation. The orchestration should ensure smooth execution of these core tasks without the inclusion of monitoring or alert systems at this stage. Prefect workflows should be modular and clearly defined to allow easy integration of future improvements.

### **7. Testing**  
Finalize all tests currently in development, focusing on critical tests necessary for core pipeline functionality. These include tests for data integrity, model training, and forecast accuracy. Individual developers should prioritize tests that validate the functionality of key pipeline components before the MVP launch.

### **8. Exclusion of Unmaintainable Code**  
Exclude unmaintainable or high-technical-debt code from the migration process. A review process should be in place to identify which legacy models or components are unsuitable for migration based on maintainability and technical debt.

### **9. Catalog Reference**  
The MVP should include most models from the old pipeline, with clear references to the existing model catalogs. These catalogs will be used to track model migration progress and ensure that all key models are accounted for during the transition to the new pipeline.

---

## **Long-Term Considerations (Post-MVP)**

The post-MVP roadmap includes the following high-priority goals:

- Addition of uncertainty estimation (approximate posterior distributions).
- Expansion of prediction targets to include additional measures of violence and conflict impacts.
- Integration of nowcasting and input/interpolation uncertainty.
- Implementation of a unified evaluation framework, followed by the rollout of an online evaluation system.
- Global expansion of PGM-level forecasts.
- Expansion of the evaluation metric roster to included all metrics decided on doing the "metric workshop"

----

## **Suggested formulation of GitHub Milestones (documented here for the purpose of PR review)**

### **1. PGM Predictions (Legacy Models)**

#### **Description**  
Produce PGM-level predictions using the majority of models from the old pipeline, focusing on consistency with the original pipeline's output.

#### **Subtasks**  
   - Migrate and implement simple stepshift models first.
   - Follow up with the implementation of hurdle models.
   
#### **Outcome**  
PGM models from the old pipeline are successfully migrated and integrated into the new pipeline, producing predictions that are consistent with the original outputs.


### **2. HydraNet PGM Predictions**

#### **Description**  
Integrate HydraNet models to produce PGM-level predictions within the new pipeline, ensuring their full deployment and operational status.

#### **Outcome**  
At least one HydraNet model is fully integrated into the new pipeline, generating accurate PGM-level predictions.

### **3. CM Predictions (Legacy Models)**

#### **Description**  
Migrate CM-level models from the old pipeline to the new pipeline, aiming for consistent predictions with the original pipeline's outputs.

#### **Subtasks**  
   - Migrate and implement simple stepshift models first.
   - Follow up with the implementation of hurdle models.
   
#### **Outcome**  
CM models from the old pipeline are successfully migrated and produce predictions consistent with the original pipeline.

### **4. Ensembles (Mean and Median)**

#### **Description**  
Implement a mean ensemble method for both PGM and CM-level models. Additionally, deploy a median ensemble as a shadow model to provide a baseline comparison.

#### **Outcome**  
Mean and median ensemble methods are implemented, with evaluation results documented and reported on Weights and Biases.

### **5. Calibration (Temporary Solution)**

#### **Description**  
Use Jim’s calibration script to temporarily align ensemble predictions at the PGM and CM levels.

#### **Outcome**  
A temporary calibration solution is in place, aligning PGM and CM ensemble predictions, with improvements planned for post-MVP development.

### **6. Prefect Orchestration**

#### **Description**  
Set up Prefect orchestration to manage the pipeline’s core tasks, including data fetching, model training, and forecast generation.

#### **Outcome**  
Prefect workflows are configured to execute data fetching, training, and forecast generation tasks, ensuring smooth pipeline operation without monitoring or alerts.

### **7. Model Catalog Update**

#### **Description**  
Update the model catalogs to reflect the status of all models included in the MVP, ensuring accurate tracking of the migration process.

#### **Outcome**  
Model catalogs are up-to-date and provide accurate references for all models integrated into the new pipeline.

### **8. Finalization of Architectural Decision Records (ADRs)**

#### **Description**  
Complete all Architectural Decision Records (ADRs) that are relevant to the MVP, ensuring that decisions are well-documented and accessible.

#### **Outcome**  
All MVP-related ADRs are finalized, providing a comprehensive record of design choices and architectural decisions.
