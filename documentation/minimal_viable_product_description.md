# **MVP Pipeline (Target Completion: Early November)**

## **Primary Goal**  
The goal of the new pipeline is to produce predictions that either match or exceed the performance of the existing pipeline while incorporating HydraNet PGM-level predictions. Although some model implementations may differ, the overall predictive performance is expected to be as good as, or better than, the previous pipeline. **Performance improvement will be assessed using specific evaluation metrics** (For now, MSLE, MSE, and MAE for regression models; AP, AUC, and Brier for classification models). These metrics will guide both the initial development and post-deployment evaluations. Additional metrics already defined elswhere will be added post MPV.

---

## **MVP Requirements and Deliverables**

### **1. PGM Predictions from Legacy Models**  
The MVP will produce PGM-level predictions from the majority of models implemented in the old pipeline. The models selected for inclusion are documented in the model [catalogs](https://github.com/prio-data/views_pipeline/tree/main/documentation/catalogs), which track the transition to the new pipeline. When possible, unmodified DARTS models will be used if they meet the project's classification performance requirements. Adaptations for each model should not exceed three days; any models requiring longer adaptation will be deprioritized. **Models that rely on the old step shifter are deemed unmaintainable and will not be included**.

> **Definition of Unmaintainable Models**:  
> - **Unmaintainable models** are those with significant technical debt or complex dependencies that hinder long-term maintenance. A model is unmaintainable if:
>   - It introduces **high technical debt** or relies on complex dependencies incompatible with DARTS or the new pipeline architecture.
>   - It uses **outdated or unsupported packages** (e.g., the legacy step shifter), posing integration, documentation, or stability challenges.
>   - It requires **extensive, custom modifications** that exceed three development days and cannot be applied across multiple models in the pipeline.
>   - It is currently **not implemented in Python**, but e.g. only implemented in R.


On short, only models that are fully implemented, clearly structured, and production-ready in Python will be included in the MVP. Models implemented in R, those requiring substantial refactoring, or those that do not meet production standards will be deprioritized.

---

### **2. HydraNet PGM Predictions**  
The HydraNet models will be integrated and deployed to produce PGM-level predictions. **At least one HydraNet model must be fully operational and generating predictions, ensuring compatibility with legacy models in the system**.

> **Clarifications**:
> - **Compatibility**: Compatibility includes both **technical integration** (ensuring HydraNet models coexist with legacy models without conflicts) and **performance alignment** (producing comparable or superior predictive accuracy and robustness).
> - **Fully Operational**: A “fully operational” HydraNet model is defined as one that reliably produces predictions in production, undergoes periodic evaluation using designated metrics (e.g., MSLE, MSE), and meets essential maintenance requirements for stability. Comprehensive evaluation and maintenance routines will be addressed post-MVP.

---

### **3. CM Predictions from Legacy Models**  
The MVP will produce CM-level predictions from most models implemented in the old pipeline, with selections documented in the model [catalogs](https://github.com/prio-data/views_pipeline/tree/main/documentation/catalogs). When feasible, unmodified DARTS models will be used. Complex adaptations for CM models will be deprioritized unless they are essential to overall system functionality and performance.

> **Clarifications and Prioritization**:  
> - **Complex Adaptations**: This refers to extensive changes to a model’s architecture or code that require unique, non-reusable adjustments (e.g., adapting non-DARTS models with custom handling for data or dependency conflicts). This also includes models not currently implemented in Python. Complex adaptations will be deprioritized if they exceed the MVP’s adaptation timeframe of three development days.
> - **Prioritization of Legacy Models**: To meet the MVP deadline, we will prioritize high-value legacy models, such as those using well-maintained and well-understood data sources.

---

### **4. Ensembles**  
The MVP will implement a mean ensemble method for aggregating predictions from both PGM and CM-level models, along with a median ensemble as a shadow model to serve as a baseline for validation and comparison.

**Ensemble Outputs**: The final mean ensemble results must be in a non-logged format for predicted fatalities. Jim’s script might need updating to ensure these results are properly integrated into the API.

---

### **5. "Calibration" (Temporary Solution)**  
Jim’s existing "calibration" script will be used **temporarily** to align ensemble predictions at the PGM and CM levels. There must also be a calibration to ensure that predicted counts are **≥ 0** (to prevent negative counts, as models like XGBoost do not inherently enforce this). For now, these calibration steps are critical for ensuring prediction quality and reliability within expected thresholds. But it should always be stressed that calibration is a post-hoc fix revealing that weaknesses of a model. As such all calibration scripts should include alarts and logs notifying the user if original vlaues are drastically or substantially changed. 

> **Known Limitations**:  
> - The current calibration approach has limitations, such as potential systematic offsets causing minor prediction inaccuracies. These limitations will be documented, and calibration results will be monitored for patterns or biases.
> - Developing a more robust calibration method will be a high-priority task post-MVP to improve model consistency and accuracy.
> - Developing models that does not require substantial calibration is a explicit goal going forward.

> **Terminology issues**
> -

---

### **6. Prefect Orchestration**  
Prefect will be implemented to orchestrate the pipeline, managing data fetching, model training, and forecast generation. Prefect workflows should be modular, allowing for easy expansion and improvements in future iterations.

---

### **7. Testing and Evaluation**  
All tests in development will be completed, focusing on essential functions like data integrity, model training, and forecast accuracy. Developers will prioritize tests that validate key pipeline components before the MVP launch.

> **Specified Evaluation Metrics**:  
> - For regression models, **Mean Squared Logarithmic Error (MSLE)**, **Mean Squared Error (MSE)**, and **Mean Absolute Error (MAE)** will be used. For classification models, **Average Precision (AP)**, **Area Under Curve (AUC)**, and **Brier Score** will serve as primary metrics. These metrics will assess both individual models and ensemble predictions, providing a baseline for accuracy and robustness.
> - Model evaluations, including those for individual and ensemble models, will be documented in Weights and Biases.
> - A full set of metrics, determined in a pre-sprint workshop, will be added post-MVP alongside a new comprehensive evaluation scheme.

---

### **8. Exclusion of Unmaintainable Code**  
Code with high technical debt or low maintainability will be excluded from the MVP. A review process will identify legacy models or components unsuitable for migration based on maintainability and technical debt considerations.

---

### **9. Catalog Reference**  
The MVP will include most models from the old pipeline, with references to existing model catalogs. These catalogs will track migration progress and ensure that all essential models are considered during the transition.

> **Additional Requirements**:
> - **Prediction Output**: The MVP will include both constituent and ensemble model outputs, stored in the **prediction store** and accessible through the API. To replace the old pipeline, flat files and pickles will be phased out in favor of a centralized storage format. Predictions will be stored in a standardized dataframe format, enabling centralization and accessibility.
> - **Mapping for Visualization**: Predictions will be formatted for compatibility with existing mapping tools, allowing immediate use for visualizations without requiring additional tools for the MVP. Mapping enhancements, while essential, will be developed post-MVP to maintain a streamlined pipeline.
> - **Evaluation**: Core evaluation processes will be embedded within the pipeline, measuring both individual models and ensemble predictions against **MSLE**, **MSE**, **MAE**, **AP**, **AUC**, and **Brier Score** metrics. Evaluations will be stored in Weights & Biases, utilizing existing infrastructure for alignment with API standards. Additional evaluation tools will be introduced post-MVP for scalable, consistent assessments.
> - **Metadata Compliance**: The MVP will meet Angelica’s API requirements for metadata inclusion, ensuring each prediction includes the necessary metadata need for the VIEWS Dashboard.

---

## **Priorities for Post-MVP Development**  
Once the MVP is complete, these steps will be prioritized to ensure long-term stability, better uncertainty management, and improved data handling.

1. **Nowcasting and Uncertainty Estimation**  
   - Develop nowcasting capabilities for short-term forecasting accuracy.
   - Refine input and interpolation uncertainty measurements to handle imputed data, improving prediction robustness and data quality.

2. **Unified Evaluation Framework For All Models (Offline and Online)**  
   - Implement a unified evaluation framework to standardize metrics, streamline evaluations, and introduce an online evaluation system and output drift detection for ongoing performance assessment using pre-defined metrics and benchmarks.

3. **Global Expansion of PGM-Level Forecasts**  
   - Extend PGM-level forecasting to a global scale, broadening applicability and utility for policy and decision-making.

4. **Expanded Evaluation Metric Roster**  
   - Add new evaluation metrics based on outcomes from the recent metric workshop, focusing on metrics that enhance precision, calibration, and reliability.

-----------------------------------------------------------------


## **MVP Requirements and Deliverables**

### **1. PGM Predictions from Legacy Models**  
Produce PGM-level predictions from the majority of models implemented in the old pipeline. The models to be included should be referenced from the model [catalogs](https://github.com/prio-data/views_pipeline/tree/main/documentation/catalogs), which track the transition to the new pipeline. Where applicable, unmodified DARTS models should be considered if their classification performance meets the project’s needs. Adaptation efforts for any individual model should not exceed three working days. Any models that cannot be adapted within this timeframe should be deprioritized for now. Unmaintainable or deprecated models will not be included in the MVP.

### **2. HydraNet PGM Predictions**  
Integrate and deploy HydraNet models to produce PGM-level predictions. At least one HydraNet model must be fully operational and producing predictions within the system, ensuring its compatibility alongside legacy models.

### **3. CM Predictions from Legacy Models**  
Produce CM-level predictions from the majority of models implemented in the old pipeline. The models to be included should be referenced from the model [catalogs](https://github.com/prio-data/views_pipeline/tree/main/documentation/catalogs), which track the transition to the new pipeline. Where applicable, unmodified DARTS models should be considered if their classification performance meets the project’s needs. Complex adaptations for CM models should be deprioritized unless they are critical for ensuring overall system functionality and performance.

### **4. Ensembles**  
Implement a mean ensemble method for aggregating predictions from both PGM and CM-level models. Additionally, deploy a median ensemble as a shadow model to serve as a baseline for comparison and validation purposes.

### **5. "Calibration" (Temporary Solution)**  
Utilize Jim’s existing "calibration" script to temporarily align ensemble predictions at the PGM and CM levels. While this solution will suffice for the MVP, developing a more robust and accurate "calibration" method will be a top priority post-MVP as Jim has marked the current solution as "hacky as hell".

### **6. Prefect Orchestration**  
Implement Prefect orchestration to manage the entire pipeline, focusing on data fetching, model training, and forecast generation. The orchestration should ensure smooth execution of these core tasks without the inclusion of monitoring or alert systems at this stage. Prefect workflows should be modular and clearly defined to allow easy integration of future improvements.

### **7. Testing**  
Finalize all tests currently in development, focusing on critical tests necessary for core pipeline functionality. These include tests for data integrity, model training, and forecast accuracy. Individual developers should prioritize tests that validate the functionality of key pipeline components before the MVP launch.

### **8. Exclusion of Unmaintainable Code**  
Exclude unmaintainable or high-technical-debt code from the migration process. A review process should be in place to identify which legacy models or components are unsuitable for migration based on maintainability and technical debt.

### **9. Catalog Reference**  
The MVP should include most models from the old pipeline, with clear references to the existing model catalogs. These catalogs will be used to track model migration progress and ensure that all key models are accounted for during the transition to the new pipeline.

