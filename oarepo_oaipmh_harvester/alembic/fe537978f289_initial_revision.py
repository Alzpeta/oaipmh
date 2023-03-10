#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Initial revision."""
from enum import Enum

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'fe537978f289'
down_revision = '007a7cd707e1'
branch_labels = ()
depends_on = None


class HarvestStatus(Enum):
    RUNNING = 'R'
    FINISHED = 'O'
    WARNING = 'W'
    FAILED = 'E'


def upgrade():
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oarepo_oaipmh_harvester',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=255), nullable=False),
    sa.Column('baseurl', sa.String(length=255), server_default='', nullable=False),
    sa.Column('metadataprefix', sa.String(length=255), server_default='oai_dc', nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('setspecs', sa.Text(), nullable=False),
    sa.Column('parser', sa.Text(), nullable=True),
    sa.Column('transformer', sa.Text(), nullable=False),
    sa.Column('max_records', sa.Integer(), nullable=True),
    sa.Column('batch_size', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_oarepo_oaipmh_harvester')),
    sa.UniqueConstraint('code', name=op.f('uq_oarepo_oaipmh_harvester_code'))
    )
    op.create_table('oarepo_oaipmh_harvester_run',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('harvester_id', sa.Integer(), nullable=True),
    sa.Column('started', sa.DateTime(), nullable=True),
    sa.Column('finished', sa.DateTime(), nullable=True),
    sa.Column('first_datestamp', sa.String(length=32), nullable=True),
    sa.Column('last_datestamp', sa.String(length=32), nullable=True),
    sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(HarvestStatus, impl=sa.String(length=1)), nullable=True),
    sa.Column('exception', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['harvester_id'], ['oarepo_oaipmh_harvester.id'], name=op.f('fk_oarepo_oaipmh_harvester_run_harvester_id_oarepo_oaipmh_harvester')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_oarepo_oaipmh_harvester_run'))
    )
    op.create_table('oarepo_oaipmh_harvester_batch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=True),
    sa.Column('harvested_records', sqlalchemy_utils.types.json.JSONType(), nullable=True),
    sa.Column('warning_records', sqlalchemy_utils.types.json.JSONType(), nullable=True),
    sa.Column('failed_records', sqlalchemy_utils.types.json.JSONType(), nullable=True),
    sa.Column('started', sa.DateTime(), nullable=True),
    sa.Column('finished', sa.DateTime(), nullable=True),
    sa.Column('status', sqlalchemy_utils.types.choice.ChoiceType(HarvestStatus, impl=sa.String(length=1)), nullable=True),
    sa.Column('exception', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['run_id'], ['oarepo_oaipmh_harvester_run.id'], name=op.f('fk_oarepo_oaipmh_harvester_batch_run_id_oarepo_oaipmh_harvester_run')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_oarepo_oaipmh_harvester_batch'))
    )
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oarepo_oaipmh_harvester_batch')
    op.drop_table('oarepo_oaipmh_harvester_run')
    op.drop_table('oarepo_oaipmh_harvester')
    # ### end Alembic commands ###
