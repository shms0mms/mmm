
from typing import List
from src.config.metadata import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String


class Transaction(Base):
	__tablename__ = 'transaction'
	id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
	from_account_number: Mapped[str] = mapped_column(String(length=16))
	to_account_number: Mapped[str] = mapped_column(String(length=16))
	amount: Mapped[float] = mapped_column(nullable=False)
	# users_ids: Mapped[List[int]] = mapped_column(ARRAY(ForeignKey(User.id)))
	# users = relationship("User", back_populates="transactions")