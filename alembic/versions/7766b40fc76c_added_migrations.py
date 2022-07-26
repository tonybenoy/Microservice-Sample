"""Added migrations

Revision ID: 7766b40fc76c
Revises: 
Create Date: 2022-02-07 19:26:40.837791

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7766b40fc76c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forms',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('published', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forms_id'), 'forms', ['id'], unique=False)
    op.create_table('form_definition',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('published', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_form_definition_id'), 'form_definition', ['id'], unique=False)
    op.create_table('form_data',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('form_definition_id', sa.Integer(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['form_definition_id'], ['form_definition.id'], ),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_form_data_id'), 'form_data', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_form_data_id'), table_name='form_data')
    op.drop_table('form_data')
    op.drop_index(op.f('ix_form_definition_id'), table_name='form_definition')
    op.drop_table('form_definition')
    op.drop_index(op.f('ix_forms_id'), table_name='forms')
    op.drop_table('forms')
    # ### end Alembic commands ###
