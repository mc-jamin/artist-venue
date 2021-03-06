"""relationship removed again

Revision ID: 00df2b52279a
Revises: 88d70b99a930
Create Date: 2022-06-03 14:04:25.838547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00df2b52279a'
down_revision = '88d70b99a930'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('artist_venue_id_fkey', 'artist', type_='foreignkey')
    op.drop_column('artist', 'venue_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('artist_venue_id_fkey', 'artist', 'venue', ['venue_id'], ['id'])
    # ### end Alembic commands ###
