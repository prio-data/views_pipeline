### Glossary

|Info| Details|
|--------------|-----------|
| Last updated | 29.07.2024|
| By author    | Simon     |

- **forecast_step**: The time increment at which predictions are made in a time series, reflecting the data's frequency (e.g., daily, monthly, yearly). This step indicates the temporal position of each forecast relative to the last observed data point. For example, forecasting 36 months into the future involves steps {0,1,2,…,35}, where step 0 represents the first forecasted period immediately following the last observed data point.

- **month_id**: A unique identifier assigned to each month in a time series, beginning with the initial observation period and continuing sequentially. For example, January 1980 is month_id 1, February 1980 is month_id 2, and so on. If the last observed month is December 2020 (month_id 492), subsequent months continue sequentially, with January 2021 as month_id 493, February 2021 as month_id 494, etc.

- **year**: The actual calendar year in which a data point or forecast occurs, such as 1980, 2021, etc.

- **forecast_start**: The temporal identifier marking the beginning of the forecast period. For instance, if the last observed month is December 2020 (month_id 492), January 2021 (month_id 493) marks the forecast_start.

- **forecast_end**: The temporal identifier marking the end of the forecast period. For example, if the forecast begins in January 2021 (month_id 493) and spans 36 months, the forecast_end would be December 2023 (month_id 528).

- **forecast_horizon**: The total duration into the future for which predictions are made, measured in the same units as the time series data. For instance, a forecast horizon of 36 months indicates predictions are made for the next 36 months following the forecast_start.

- **forecast_lead_time**: The duration between when a forecast is made and when the predicted event occurs. It reflects how far in advance the forecast is provided relative to the event being predicted. For example, a forecast made in January 2021 for the month of March 2021 has a forecast lead time of 2 months.

This glossary format should provide a clear and structured reference for anyone working with or interpreting the time series data and forecasts in your context.