"""empty message

Revision ID: 4ad5671ea04c
Revises: None
Create Date: 2015-05-30 10:40:48.209990

"""

# revision identifiers, used by Alembic.
revision = '4ad5671ea04c'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incentive', sa.Column('approved', sa.Boolean(), nullable=True))
    op.add_column('incentive', sa.Column('approved_by', sa.String(length=50), nullable=True))
    op.add_column('incentive', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('timestamp', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'timestamp')
    op.drop_column('incentive', 'timestamp')
    op.drop_column('incentive', 'approved_by')
    op.drop_column('incentive', 'approved')
    ### end Alembic commands ###