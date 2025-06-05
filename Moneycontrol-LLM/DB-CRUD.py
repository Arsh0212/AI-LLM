from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import select, insert, update, delete

class Database_Management:

    def __init__(self):
        self.engine = create_engine("postgresql://postgres:Aqua2002!!!@localhost:5432/Gold",echo=False)
        self.metadata = MetaData()
        self.news_articles = Table("news_articles", self.metadata, autoload_with=self.engine)

    def select_data(self,Filter):
        with self.engine.connect() as conn:
            stmt = select(self.news_articles.c.cont).where(self.news_articles.c.title.ilike('%'+Filter+'%'))
            result = conn.execute(stmt)
            return result

    def select_all_data(self):
        with self.engine.connect() as conn:
            stmt = select(self.news_articles)
            result = conn.execute(stmt)
            return result

    def insert_data(self,title,content):
        with self.engine.connect() as conn:
            stmt = insert(self.news_articles).values(
                title=title,
                cont = content
            )
            conn.execute(stmt)
            conn.commit()
    
    def update_data(self):
        with self.engine.connect() as conn:
            stmt = update(self.news_articles).where(self.news_articles.c.id == 1).values(title="Updated Title")
            conn.execute(stmt)
            conn.commit()

    def delete_data(self):
        with self.engine.connect() as conn:
            stmt = delete(self.news_articles).where(self.news_articles.c.id == 1)
            conn.execute(stmt)
            conn.commit()





