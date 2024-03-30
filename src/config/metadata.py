from sqlalchemy.orm import  DeclarativeBase, mapped_column, Mapped
class Base(DeclarativeBase):
	id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)


