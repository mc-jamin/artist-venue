"""relationship reestablished

Revision ID: 88d70b99a930
Revises: 59988b665639
Create Date: 2022-06-03 14:01:44.780609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88d70b99a930'
down_revision = '59988b665639'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('venue_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'artist', 'venue', ['venue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'artist', type_='foreignkey')
    op.drop_column('artist', 'venue_id')
    # ### end Alembic commands ###
