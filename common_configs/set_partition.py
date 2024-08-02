from ingester3.ViewsMonth import ViewsMonth

def get_partitioner_dict(partion, step=36):

    """Returns the partitioner_dict for the given partion."""

    if partion == 'calibration':

        # calib_partitioner according to Hegre et al  2021: train 121-396 = 01/01/1990-12/31/2012. val: 397- 432 = 01/01/2013-31/12/2015
        partitioner_dict = {"train":(121,396),"predict":(397,432)} #!!! 444 was specified by HH, but 444 = 2016-12-31 and not 2015-12-31....

    if partion == 'testing':

        # test_partitioner according to Hegre et al  2021: train 121-432 = 01/01/1990-12/31/2015. val: 433-468 = 01/01/2017-31/12/2018
        partitioner_dict = {"train":(121,432),"predict":(433,468)} #!!! 444 was specified by HH, but 444 = 2016-12-31 and not 2015-12-31 and 492 = 2020-12-31 and not 2018-12-31 (468)
        # note that since hydranet was set to only do 36 months, the end month of the test set was not important as long as it is beyond 36 ahead. 

    if partion == 'forecasting':

        month_last =  ViewsMonth.now().id - 2 # minus 2 because the current month is not yet available. Verified but can be tested by chinging this and running the check_data notebook.

        partitioner_dict = {"train":(121, month_last),"predict":(month_last +1, month_last + 1 + step)}  # is it even meaningful to have a predict partition for forecasting? if not you can remove steps

    print('partitioner_dict', partitioner_dict) 

    return partitioner_dict

# currently these differ from the ones in the config_data_partitions.py file for the stepshifted models (see below). This needs to be sorted out asap.

#    data_partitions = {
#        'calib_partitioner_dict': {"train": (121, 396), "predict": (409, 456)},   # Does not make sense that the eval set starts at 409, it should start at 397, no?
#        'test_partitioner_dict': {"train": (121, 456), "predict": (457, 504)},
#        'future_partitioner_dict': {"train": (121, 504), "predict": (529, 529)}, # NO HARD CODIGN THE FUTURE START DATE
#        'FutureStart': 529, #Jan 24 # THIS SHOULD NOT BE HARD CODED!!!! Whatever the right partitions are for calibration and testing, the forecasting should be automatically infered from the current date.
#    }



# Suggested Rolling forecasting origin eval scheme: But what about the gap?(!!!) Should we have a one month gap betwee train and validation? 
#| Evaluation | Calibration validation start | Calibration validation end | Test validation start | Test validation end |
#|------------|------------------------------|----------------------------|-----------------------|---------------------|
#| 0          | 432                          | 467                        | 433                   | 468                 |
#| 1          | 433                          | 468                        | 434                   | 469                 |
#| 2          | 434                          | 469                        | 435                   | 470                 |
#| 3          | 435                          | 470                        | 436                   | 471                 |
#| 4          | 436                          | 471                        | 437                   | 472                 |
#| 5          | 437                          | 472                        | 438                   | 473                 |
#| 6          | 438                          | 473                        | 439                   | 474                 |
#| 7          | 439                          | 474                        | 440                   | 475                 |
#| 8          | 440                          | 475                        | 441                   | 476                 |
#| 9          | 441                          | 476                        | 442                   | 477                 |
#| 10         | 442                          | 477                        | 443                   | 478                 |
#| 11         | 443                          | 478                        | 444                   | 479                 |
#| 12         | 444                          | 479                        | 445                   | 480                 |
#| 13         | 445                          | 480                        | 446                   | 481                 |
#| 14         | 446                          | 481                        | 447                   | 482                 |
#| 15         | 447                          | 482                        | 448                   | 483                 |
#| 16         | 448                          | 483                        | 449                   | 484                 |
#| 17         | 449                          | 484                        | 450                   | 485                 |
#| 18         | 450                          | 485                        | 451                   | 486                 |
#| 19         | 451                          | 486                        | 452                   | 487                 |
#| 20         | 452                          | 487                        | 453                   | 488                 |
#| 21         | 453                          | 488                        | 454                   | 489                 |
#| 22         | 454                          | 489                        | 455                   | 490                 |
#| 23         | 455                          | 490                        | 456                   | 491                 |
#| 24         | 456                          | 491                        | 457                   | 492                 |
#| 25         | 457                          | 492                        | 458                   | 493                 |
#| 26         | 458                          | 493                        | 459                   | 494                 |
#| 27         | 459                          | 494                        | 460                   | 495                 |
#| 28         | 460                          | 495                        | 461                   | 496                 |
#| 29         | 461                          | 496                        | 462                   | 497                 |
#| 30         | 462                          | 497                        | 463                   | 498                 |
#| 31         | 463                          | 498                        | 464                   | 499                 |
#| 32         | 464                          | 499                        | 465                   | 500                 |
#| 33         | 465                          | 500                        | 466                   | 501                 |
#| 34         | 466                          | 501                        | 467                   | 502                 |
#| 35         | 467                          | 502                        | 468                   | 503                 |

# UNTESTED CODE BELOW TO GENERATE THE ABOVE TABLE AS A PADAS DATAFRAME
# import pandas as pd
# 
# def generate_rolling_forecast_df(initial_start_index, num_evaluations=36, step=1):
#     # Calculate the start and end indices for each evaluation
#     start_indices = [initial_start_index + i for i in range(num_evaluations)]
#     end_indices = [start + 35 for start in start_indices]
#     test_start_indices = [start + 1 for start in start_indices]
#     test_end_indices = [end + 1 for end in end_indices]
# 
#     # Create the DataFrame
#     df = pd.DataFrame({
#         "Evaluation": range(num_evaluations),
#         "Calibration validation start": start_indices,
#         "Calibration validation end": end_indices,
#         "Test validation start": test_start_indices,
#         "Test validation end": test_end_indices
#     })
# 
#     return df
# 
# # Example usage
# example_df = generate_rolling_forecast_df(432)
# print(example_df)