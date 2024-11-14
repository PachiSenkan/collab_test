from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class DatasetLite(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pk: int = Field(..., description="ID of dataset")
    description: str | None = None
    author: str | None = None
    original_id: int = Field(..., description="ID of original dataset")


class Dataset(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pk: int = Field(..., description="ID of dataset")
    description: str | None = None
    author: str | None = None
    original_id: int = Field(..., description="ID of original dataset")
    created_at: datetime
    updated_at: datetime
    parent_dataset_id: int | None = Field(None, description="ID родительского набора")
    children_datasets: list[DatasetLite | None]
    dataset: list[dict[str, Any]]


class DatasetQuery(BaseModel):
    pk: int = Field(None, description="ID of dataset")
    description: str | None = None
    author: str | None = None
    original_id: int = Field(..., description="ID of original dataset")


class DatasetUpdate(BaseModel):
    description: str | None = None
    author: str | None = None
    original_id: int = Field(..., description="ID of original dataset")
    dataset: list[dict[str, Any]]


class DatasetCreate(BaseModel):
    description: str | None = None
    author: str | None = None
    original_id: int = Field(..., description="ID of original dataset")
    parent_dataset_id: int | None = Field(None, description="ID родительского набора")
    dataset: list[dict[str, Any]]
