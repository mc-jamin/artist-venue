"""full schema generated

Revision ID: f62300368c57
Revises: d0e87b7a827b
Create Date: 2022-06-04 09:13:16.001789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f62300368c57'
down_revision = 'd0e87b7a827b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('address', sa.String(length=120), nullable=True))
    op.add_column('artist', sa.Column('website_link', sa.String(length=500), nullable=True))
    op.add_column('artist', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('website_link', sa.String(length=500), nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_description')
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'website_link')
    op.drop_column('venue', 'genres')
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'seeking_talent')
    op.drop_column('artist', 'website_link')
    op.drop_column('artist', 'address')
    # ### end Alembic commands ###
