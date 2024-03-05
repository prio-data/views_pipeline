"""
views_stepshift
==========

This package collects views related tools and utilities used when planning,
training and predicting.

classes:
    ViewsRun:
        Class that encapsulates StepshiftedModels and DataPartitioner objects
        to provide a nice API for training and producing predictions.
    StepshiftedModels:
        Model class from the stepshift package that lets you train stepshifted
        models.
    DataPartitioner:
        Utility class for subsetting data in time, that lets you define
        tranining and testing periods, as well as do operations to ensure no
        overlap exists between these periods.
    ModelMetadata:
        Class used to specify metadata for trained model objects.

modules:
    utilities: Various utility functions ported from views 2
    run: Defines the ViewsRun class
    validation: Functions used internally to validate data

Each class and module mentioned here has more documentation. Use the help()
function.

"""
import logging

from .run import ViewsRun

from stepshift.views import StepshiftedModels
from views_partitioning.data_partitioner import DataPartitioner
from views_schema.models import ModelMetadata
