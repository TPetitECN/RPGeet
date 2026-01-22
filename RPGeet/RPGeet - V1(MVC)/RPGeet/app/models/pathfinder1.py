from app.models.core import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

# Schema: pathfinder1

class P1NSource(db.Model):
    __tablename__ = 'n_sources'
    __table_args__ = {'schema': 'pathfinder1'}
    
    source_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    core_source_id: Mapped[int] = mapped_column(nullable=False)

class P1NClassStatsCategory(db.Model):
    __tablename__ = 'n_class_stats_categories'
    __table_args__ = {'schema': 'pathfinder1'}
    
    class_stats_category_id: Mapped[int] = mapped_column(primary_key=True)
    class_stats_category_name: Mapped[str] = mapped_column(db.String(15), nullable=False)

class P1ClassStats(db.Model):
    __tablename__ = 'class_stats'
    __table_args__ = {'schema': 'pathfinder1'}
    
    class_stats_id: Mapped[int] = mapped_column(primary_key=True)
    fortitude_save_cat: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.n_class_stats_categories.class_stats_category_id'), nullable=False)
    reflex_save_cat: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.n_class_stats_categories.class_stats_category_id'), nullable=False)
    will_save_cat: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.n_class_stats_categories.class_stats_category_id'), nullable=False)
    base_battle_bonus: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.n_class_stats_categories.class_stats_category_id'), nullable=False)

class P1ModifierType(db.Model):
    __tablename__ = 'modifier_types'
    __table_args__ = {'schema': 'pathfinder1'}
    
    modifier_type_id: Mapped[int] = mapped_column(primary_key=True)
    modifier_type_name: Mapped[str] = mapped_column(db.String(31), nullable=False)

class P1Skill(db.Model):
    __tablename__ = 'skills'
    __table_args__ = {'schema': 'pathfinder1'}
    
    id_skill: Mapped[int] = mapped_column(primary_key=True)
    skill_name: Mapped[str] = mapped_column(db.String(31), nullable=False)
    skill_short_description: Mapped[str] = mapped_column(db.String(255), nullable=False)

class P1DescriptiveFeatures(db.Model):
    __tablename__ = 'descriptive_features'
    __table_args__ = {'schema': 'pathfinder1'}
    
    descriptive_features_id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(db.String(1), nullable=False)
    height: Mapped[float] = mapped_column(db.Float, nullable=False)
    weight: Mapped[float] = mapped_column(db.Float, nullable=False)
    hair_short_desc: Mapped[str] = mapped_column(db.String(31), nullable=False)
    eyes_short_desc: Mapped[str] = mapped_column(db.String(31), nullable=False)
    skin_short_desc: Mapped[str] = mapped_column(db.String(31), nullable=False)

class P1Statistics(db.Model):
    __tablename__ = 'statistics'
    __table_args__ = {'schema': 'pathfinder1'}
    
    statistics_id: Mapped[int] = mapped_column(primary_key=True)
    max_hp: Mapped[int] = mapped_column(nullable=False)
    lethal_dmg: Mapped[int] = mapped_column(nullable=False)
    non_lethal_dmg: Mapped[int] = mapped_column(nullable=False)
    base_strength: Mapped[Optional[int]]
    base_dexterity: Mapped[Optional[int]]
    base_constitution: Mapped[Optional[int]]
    base_intelligence: Mapped[Optional[int]]
    base_wisdom: Mapped[Optional[int]]
    base_charisma: Mapped[Optional[int]]

class P1Source(db.Model):
    __tablename__ = 'sources'
    __table_args__ = {'schema': 'pathfinder1'}
    
    source_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(1024), nullable=False)
    core_source_id: Mapped[int] = mapped_column(nullable=False)

class P1Deity(db.Model):
    __tablename__ = 'deities'
    __table_args__ = {'schema': 'pathfinder1'}
    
    deity_id: Mapped[int] = mapped_column(primary_key=True)
    deity_name: Mapped[str] = mapped_column(nullable=False)
    deity_alignment: Mapped[str] = mapped_column(db.String(2), nullable=False)
    source_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.sources.source_id'), nullable=False)

class P1Race(db.Model):
    __tablename__ = 'races'
    __table_args__ = {'schema': 'pathfinder1'}
    
    race_id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.sources.source_id'), nullable=False)

class P1Character(db.Model):
    __tablename__ = 'character'
    __table_args__ = {'schema': 'pathfinder1'}
    
    character_id: Mapped[int] = mapped_column(primary_key=True)
    race_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.races.race_id'), nullable=False)
    alignement: Mapped[str] = mapped_column(db.String(2), nullable=False, default='N')
    statistics_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.statistics.statistics_id'), nullable=False)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    descriptive_features_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.descriptive_features.descriptive_features_id'), nullable=False)

    # Relationships
    race = db.relationship('P1Race')
    statistics = db.relationship('P1Statistics')
    descriptive_features = db.relationship('P1DescriptiveFeatures')
    
    modifiers = db.relationship('P1Modifier', back_populates='character')
    skills = db.relationship('P1RSkillCharacter', back_populates='character')
    classes = db.relationship('P1RClassesCharacter', back_populates='character')
    deities = db.relationship('P1RCharacterDeity', back_populates='character')

class P1Modifier(db.Model):
    __tablename__ = 'modifiers'
    __table_args__ = {'schema': 'pathfinder1'}
    
    id_modifier: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.character.character_id'), nullable=False)
    modifier_type_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.modifier_types.modifier_type_id'), nullable=False)
    value: Mapped[int] = mapped_column(nullable=False, default=0)
    duration: Mapped[Optional[int]] = mapped_column(default=0)

    character = db.relationship('P1Character', back_populates='modifiers')
    modifier_type = db.relationship('P1ModifierType')

class P1RModifierOrigin(db.Model):
    __tablename__ = 'r_modifier_origin'
    __table_args__ = {'schema': 'pathfinder1'}
    
    modifier_origin_id: Mapped[int] = mapped_column(primary_key=True)
    id_modifier: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.modifiers.id_modifier'), nullable=False)

class P1RSkillCharacter(db.Model):
    __tablename__ = 'r_skill_character'
    __table_args__ = {'schema': 'pathfinder1'}
    
    id_skill: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.skills.id_skill'), primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.character.character_id'), primary_key=True)
    proficiency: Mapped[bool] = mapped_column(nullable=False, default=False)
    base_score: Mapped[int] = mapped_column(nullable=False, default=0)

    character = db.relationship('P1Character', back_populates='skills')
    skill = db.relationship('P1Skill')

class P1RCharacterDeity(db.Model):
    __tablename__ = 'r_character_deity'
    __table_args__ = {'schema': 'pathfinder1'}
    
    id_character_deity: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.character.character_id'), nullable=False)
    deity_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.deities.deity_id'), nullable=False)

    character = db.relationship('P1Character', back_populates='deities')
    deity = db.relationship('P1Deity')

class P1Class(db.Model):
    __tablename__ = 'classes'
    __table_args__ = {'schema': 'pathfinder1'}
    
    class_id: Mapped[int] = mapped_column(primary_key=True)
    class_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    source_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.sources.source_id'), nullable=False)
    class_stats_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.class_stats.class_stats_id'), nullable=False)

    class_stats = db.relationship('P1ClassStats')

class P1RClassesCharacter(db.Model):
    __tablename__ = 'r_classes_character'
    __table_args__ = {'schema': 'pathfinder1'}
    
    id_class_character: Mapped[int] = mapped_column(primary_key=True)
    class_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.classes.class_id'), nullable=False)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('pathfinder1.character.character_id'), nullable=False)
    main_class: Mapped[bool] = mapped_column(nullable=False)
    class_level: Mapped[int] = mapped_column(nullable=False, default=1)

    character = db.relationship('P1Character', back_populates='classes')
    class_ = db.relationship('P1Class')
