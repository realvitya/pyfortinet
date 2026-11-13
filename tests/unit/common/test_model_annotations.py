"""Every model's runtime annotations must resolve, including nested and recursive types."""

import importlib
import inspect
import pkgutil

import pytest
from pydantic import BaseModel

import pyfortinet


def package_models():
    """Find locally defined models and embedded models without testing reexports twice."""
    models = set()

    def collect(model):
        if model in models:
            return
        models.add(model)
        for value in vars(model).values():
            if inspect.isclass(value) and issubclass(value, BaseModel) and value.__module__ == model.__module__:
                collect(value)

    for info in pkgutil.walk_packages(pyfortinet.__path__, pyfortinet.__name__ + "."):
        module = importlib.import_module(info.name)
        for value in vars(module).values():
            if inspect.isclass(value) and issubclass(value, BaseModel) and value.__module__ == module.__name__:
                collect(value)

    return sorted(models, key=lambda model: (model.__module__, model.__qualname__))


@pytest.mark.parametrize("model", package_models(), ids=lambda model: model.__module__ + "." + model.__qualname__)
def test_model_annotations_resolve_for_validation_and_serialization(model):
    # Rebuilding also catches unresolved forward references hidden by cached schemas.
    assert model.model_rebuild(force=True)
    for mode in ("validation", "serialization"):
        model.model_json_schema(mode=mode)
