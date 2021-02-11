"""add parse history table

Revision ID: 5f963aa0a597
Revises: 1cf350bc4e60
Create Date: 2020-09-29 09:44:12.956946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f963aa0a597'
down_revision = '1cf350bc4e60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parsehistory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tournament_title', sa.String(), nullable=True),
    sa.Column('tournament_link', sa.String(), nullable=True),
    sa.Column('tournament_year', sa.Integer(), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='atptennis'
    )
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('country_code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='atptennis'
    )
    op.create_table('tournament',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='atptennis'
    )
    op.create_table('entrant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tournament_id', sa.Integer(), nullable=True),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('player_seed', sa.Integer(), nullable=True),
    sa.Column('player_result', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['atptennis.player.id'], ),
    sa.ForeignKeyConstraint(['tournament_id'], ['atptennis.tournament.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='atptennis'
    )
    op.create_table('matchup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tournament_id', sa.Integer(), nullable=True),
    sa.Column('player1_id', sa.Integer(), nullable=True),
    sa.Column('player2_id', sa.Integer(), nullable=True),
    sa.Column('round_num', sa.Integer(), nullable=True),
    sa.Column('winner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player1_id'], ['atptennis.player.id'], ),
    sa.ForeignKeyConstraint(['player2_id'], ['atptennis.player.id'], ),
    sa.ForeignKeyConstraint(['tournament_id'], ['atptennis.tournament.id'], ),
    sa.ForeignKeyConstraint(['winner_id'], ['atptennis.player.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='atptennis'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('matchup', schema='atptennis')
    op.drop_table('entrant', schema='atptennis')
    op.drop_table('tournament', schema='atptennis')
    op.drop_table('player', schema='atptennis')
    op.drop_table('parsehistory', schema='atptennis')
    # ### end Alembic commands ###