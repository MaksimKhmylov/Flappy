from peewee import Model, CharField, IntegerField, SqliteDatabase

db = SqliteDatabase('score.db')


class HighScore(Model):
    player_name = CharField(max_length=64)
    score = IntegerField()

    class Meta:
        database = db

    def __str__(self):
        return f'{self.player_name} -> {self.score}'

def create_db():
    tables = (HighScore,)
    if db.table_exists(tables):
        return
    db.create_tables(tables)


def save_to_db(player_name, score):
    HighScore.create(player_name=player_name, score=score)

def get_top_players(count=10):
    return HighScore.select().order_by(HighScore.score.desc())[:count]

def get_top_player():
    return HighScore.select().order_by(HighScore.score.desc())[0]
