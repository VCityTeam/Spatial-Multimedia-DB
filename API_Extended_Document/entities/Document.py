#!/usr/bin/env python3
# coding: utf8

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from util.db_config import Base
from entities.Entity import Entity

from entities.Visualisation import Visualisation
from entities.ValidDoc import ValidDoc
from entities.Position import Position, LEVEL_MIN
from entities.ToValidateDoc import ToValidateDoc


class Document(Entity, Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer,
                     ForeignKey("user.id"),
                     nullable=False)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)
    refDate = Column(DateTime(timezone=True))
    publicationDate = Column(DateTime(timezone=True))
    type = Column(String)
    file = Column(String)
    originalName = Column(String)

    comments = relationship("Comment",
                            cascade="all, delete-orphan")

    valid_doc = relationship("ValidDoc",
                             uselist=False,
                             cascade="all, delete-orphan")

    to_validate_doc = relationship("ToValidateDoc",
                                   uselist=False,
                                   cascade="all, delete-orphan")

    visualization = relationship("Visualisation",
                                 uselist=False,
                                 cascade="all, delete-orphan")

    def __init__(self, attributes):
        self.visualization = Visualisation()
        if Document.is_allowed(attributes):
            self.valid_doc = ValidDoc()
        else:
            self.to_validate_doc = ToValidateDoc()

    def validate(self, attributes):
        self.valid_doc = ValidDoc()
        self.valid_doc.update(attributes)

    def update_initial(self, attributes):
        self.visualization.update(attributes)
        for attKey, attVal in attributes.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
        if Document.is_allowed(attributes):
            self.valid_doc.update(attributes)
        else:
            self.to_validate_doc.update(attributes)

        return self

    def update(self, attributes):
        self.visualization.update(attributes)
        for attKey, attVal in attributes.items():
            if hasattr(self, attKey):
                setattr(self, attKey, attVal)
            if self.valid_doc:
                self.valid_doc.update(attributes)
            if self.to_validate_doc:
                self.to_validate_doc.update(attributes)
        return self

    @staticmethod
    def is_allowed(auth_info):
        role = auth_info['position']['label']
        level = Position.get_clearance_level(role)
        return level > LEVEL_MIN

    def is_owner(self, auth_info):
        return auth_info['user_id'] == self.user_id
