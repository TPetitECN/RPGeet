from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.core import db, GameSystem, Source
from ._aux import admin_required
from sqlalchemy import text

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/systems')
@admin_required
def list_systems():
    """
    List all game systems for admin management.
    """
    systems = GameSystem.query.all()
    return render_template('admin/systems.html', systems=systems)

@admin_bp.route('/system/edit/', defaults={'system_id': None}, methods=['GET', 'POST'])
@admin_bp.route('/system/edit/<int:system_id>', methods=['GET', 'POST'])
@admin_required
def edit_system(system_id):
    """
    Create or edit a game system.
    
    :param system_id: The ID of the system to edit (None for creation)
    :type system_id: int or None
    """
    system = GameSystem.query.get(system_id) if system_id else None

    sources = Source.query.filter_by(system_id=system_id).all() if system else []
    
    if request.method == 'POST':
        name = request.form.get('name')
        schema_name = request.form.get('schema_name')

        if not system:
            system = GameSystem(name=name, schema_name=schema_name)
            db.session.add(system)
            
            try:
                # Create the schema for the new game system
                db.session.execute(text(f"""
                CREATE SCHEMA IF NOT EXISTS {schema_name}
                    AUTHORIZATION CURRENT_USER;
                CREATE SEQUENCE {schema_name}.n_sources_source_id_seq;

                CREATE TABLE {schema_name}.N_Sources (
                                source_id INTEGER NOT NULL DEFAULT nextval('{schema_name}.n_sources_source_id_seq'),
                                name VARCHAR NOT NULL,
                                core_source_id INTEGER NOT NULL,
                                CONSTRAINT n_sources_pk PRIMARY KEY (source_id)

                );

                ALTER SEQUENCE {schema_name}.n_sources_source_id_seq OWNED BY {schema_name}.N_Sources.source_id;

                ALTER TABLE {schema_name}.N_Sources ADD CONSTRAINT pf1_sources_core_sources_fk
                FOREIGN KEY (core_source_id)
                REFERENCES core.N_Sources (source_id)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION
                NOT DEFERRABLE;
                """))
                flash(f"Schema {schema_name} created successfully.")
            except Exception as e:
                db.session.rollback()
                flash(f"Error creating schema: {e}", "error")
                return render_template('admin/edit_system.html', system=system, sources=sources)
        else:
            system: GameSystem
            system.name = name
        
        db.session.commit()
        return redirect(url_for('admin.list_systems'))
    
    return render_template('admin/edit_system.html', system=system, sources=sources)

@admin_bp.route('/system/<int:system_id>/source/add', methods=['POST'])
@admin_required
def add_source(system_id):
    system = GameSystem.query.get_or_404(system_id)
    name = request.form.get('source_name')
    flash(f"Adding source '{name}' to system ID {system_id}")
    if system:
        system: GameSystem
        new_source_core = Source(name=name, system_id=system_id)
        db.session.add(new_source_core)
        db.session.commit()
        flash(f"Source '{name}' added.")
        
        sql = text(f"""
            INSERT INTO {system.schema_name}.n_sources (name, core_source_id)
            VALUES (:name, :core_id)
        """)
        db.session.execute(sql, {"name": name, "core_id": new_source_core.source_id})
        
        db.session.commit()
        flash(f"Source '{name}' added to core and {system.schema_name}.")
    
    return redirect(url_for('admin.edit_system', system_id=system_id))

@admin_bp.route('/source/<int:source_id>/delete', methods=['POST'])
@admin_required
def delete_source(source_id):
    source = Source.query.get_or_404(source_id)
    sid = source.system_id
    db.session.delete(source)
    db.session.commit()
    flash("Source deleted.")
    return redirect(url_for('admin.edit_system', system_id=sid))