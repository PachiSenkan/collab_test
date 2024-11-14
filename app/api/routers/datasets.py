from fastapi import APIRouter, Query, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import schemas
from app.core.session import get_db_session
from app.api.service import datasets as dataset_service

datasets_router = APIRouter(prefix="/datasets", tags=["Datasets"])


@datasets_router.get("", status_code=status.HTTP_200_OK)
async def hello_world(hello_message: str | None = "Hello World!") -> dict:
    return {"message": hello_message}


@datasets_router.post("/create")
async def dataset_create(
    dataset: schemas.DatasetCreate, session: AsyncSession = Depends(get_db_session)
) -> schemas.Dataset:
    new_dataset = await dataset_service.create_dataset(dataset.model_dump(), session)
    return new_dataset


@datasets_router.get("/")
async def datasets_list(
    session: AsyncSession = Depends(get_db_session),
) -> list[schemas.DatasetLite]:
    datasets = await dataset_service.get_all_datasets(session)
    return datasets


@datasets_router.get("/original/{original_id}")
async def dataset_get_by_original_id(
    original_id: int, session: AsyncSession = Depends(get_db_session)
) -> list[schemas.DatasetLite]:
    datasets = await dataset_service.get_datasets_by_original_id(original_id, session)
    return datasets


@datasets_router.get("/{pk}")
async def dataset_get_by_pk(
    pk: int, session: AsyncSession = Depends(get_db_session)
) -> schemas.Dataset:
    datasets = await dataset_service.get_dataset_by_pk(pk, session)
    return datasets


@datasets_router.put("/update/{pk}")
async def dataset_update(
    pk: int,
    query_dataset: schemas.DatasetUpdate,
    create_child: bool | None = False,
    session: AsyncSession = Depends(get_db_session),
) -> schemas.Dataset:
    updated_dataset = await dataset_service.update_dataset(
        pk, query_dataset.model_dump(exclude_none=True), create_child, session
    )
    return updated_dataset
