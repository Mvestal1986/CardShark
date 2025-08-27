"""Database models for TCGScan."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    """Base class for all models."""


engine = create_engine(settings.DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, future=True
)


class Card(Base):
    """Trading card with metadata from external APIs."""

    __tablename__ = "cards"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False, index=True)
    set_name: str | None = Column(String)
    set_code: str | None = Column(String, index=True)
    collector_number: str | None = Column(String)
    image_url: str | None = Column(String)
    mana_cost: str | None = Column(String)
    type_line: str | None = Column(String)
    rarity: str | None = Column(String)
    oracle_text: str | None = Column(String)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    price_snapshots = relationship(
        "PriceSnapshot", back_populates="card", cascade="all, delete-orphan"
    )
    legalities = relationship(
        "Legality", back_populates="card", cascade="all, delete-orphan"
    )


class PriceSnapshot(Base):
    """Daily pricing information for a card."""

    __tablename__ = "price_snapshots"

    id: int = Column(Integer, primary_key=True)
    card_id: int = Column(ForeignKey("cards.id"), nullable=False)
    source: str = Column(String, nullable=False)
    usd: float | None = Column(Float)
    usd_foil: float | None = Column(Float)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    card = relationship("Card", back_populates="price_snapshots")


class Legality(Base):
    """Legality status of a card for a specific format."""

    __tablename__ = "legalities"

    card_id: int = Column(ForeignKey("cards.id"), primary_key=True)
    format: str = Column(String, primary_key=True)
    status: str = Column(String, nullable=False)

    card = relationship("Card", back_populates="legalities")


class User(Base):
    """Registered user of the application."""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=True)

    collection = relationship(
        "UserCard", back_populates="user", cascade="all, delete-orphan"
    )
    decks = relationship("Deck", back_populates="owner", cascade="all, delete-orphan")


class UserCard(Base):
    """Association table for cards owned by a user."""

    __tablename__ = "user_cards"

    user_id: int = Column(ForeignKey("users.id"), primary_key=True)
    card_id: int = Column(ForeignKey("cards.id"), primary_key=True)
    quantity: int = Column(Integer, default=1)
    is_foil: bool = Column(Boolean, default=False)
    condition: str | None = Column(String)

    user = relationship("User", back_populates="collection")
    card = relationship("Card")


class Deck(Base):
    """Deck built from cards in a user's collection."""

    __tablename__ = "decks"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    format: str | None = Column(String)
    owner_id: int = Column(ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="decks")
    cards = relationship(
        "DeckCard", back_populates="deck", cascade="all, delete-orphan"
    )


class DeckCard(Base):
    """Association table linking cards to decks with a quantity."""

    __tablename__ = "deck_cards"

    deck_id: int = Column(ForeignKey("decks.id"), primary_key=True)
    card_id: int = Column(ForeignKey("cards.id"), primary_key=True)
    quantity: int = Column(Integer, default=1)

    deck = relationship("Deck", back_populates="cards")
    card = relationship("Card")


def get_session():
    """Provide a transactional scope around a series of operations."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

