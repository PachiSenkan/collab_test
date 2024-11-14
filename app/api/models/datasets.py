from datetime import datetime
from typing import Any, Optional

from sqlalchemy import JSON, ForeignKey, func, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Datasets(Base):
    __tablename__ = "datasets"

    pk: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]]
    author: Mapped[Optional[str]]
    original_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    parent_dataset_id: Mapped[Optional[int]] = mapped_column(ForeignKey("datasets.pk"))

    children_datasets: Mapped[list["Datasets"]] = relationship(
        "Datasets", back_populates="parent_dataset", lazy="joined", join_depth=1
    )
    parent_dataset: Mapped[Optional["Datasets"]] = relationship(
        "Datasets",
        back_populates="children_datasets",
        remote_side=pk,
        lazy="joined",
        join_depth=1,
    )
    # dataset: Mapped[list[dict[str, Any]]] = mapped_column(ARRAY(JSON))
    dataset: Mapped[dict[str, Any]] = mapped_column(JSON)
