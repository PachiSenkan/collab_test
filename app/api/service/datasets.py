from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.datasets import Datasets


async def get_datasets_by_original_id(original_id: int, session: AsyncSession):
    datasets = await session.scalars(
        select(Datasets).where(Datasets.original_id == original_id)
    )
    return list(datasets.unique().all())


async def get_dataset_by_pk(pk: int, session: AsyncSession):
    dataset = await session.scalar(select(Datasets).where(Datasets.pk == pk))
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset with pk {pk} not found",
        )
    return dataset


async def get_all_datasets(session: AsyncSession):
    datasets = await session.scalars(select(Datasets))
    return list(datasets.unique().all())


async def create_dataset(query_dataset: dict[str, Any], session: AsyncSession):
    dataset_instance = Datasets(**query_dataset)
    session.add(dataset_instance)
    await session.commit()
    await session.refresh(dataset_instance)
    return dataset_instance


async def update_dataset(
    pk: int,
    query_dataset: dict[str, Any],
    create_child: bool | None,
    session: AsyncSession,
):
    instance = await get_dataset_by_pk(pk, session)
    if create_child:
        new_instance = Datasets(
            author=instance.author,
            description=instance.description,
            original_id=instance.original_id,
            dataset=instance.dataset,
        )
        for var, value in query_dataset.items():
            print(f"{var}\n{value}\n")
            if value:
                setattr(new_instance, var, value)
        new_instance.parent_dataset = instance
        session.add(new_instance)
        await session.commit()
        await session.refresh(new_instance)
        return new_instance
    for var, value in query_dataset.items():
        if value:
            setattr(instance, var, value)
    await session.commit()
    await session.refresh(instance)
    return instance


# async def get_or_create_telegram_user(query_user: dict, session: AsyncSession):
#     existing_user = await get_telegram_user_by_telegram_id(query_user["id"], session)
#     # Добавить обновление того что изменилось если уже есть
#     if existing_user:
#         return existing_user
#     created_user = await create_telegram_user(query_user, session)

#     return created_user
