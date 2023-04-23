from sqlalchemy import create_engine, text, MetaData
import datetime as dt


class SQLModel:
    def __init__(self, url: str, user: str, password: str):
        conn_string = f"postgresql://{user}:{password}@{url}/scanner"

        self._engine = create_engine(conn_string, echo=False, future=True)
        self._engine.connect()

    def add_file(self, file_hash: str, file_path: str):
        '''Add a file to the database'''

        stmt = text(
            '''
                    INSERT INTO files (file_hash, file_path, date_added)
                    VALUES (:file_hash, :file_path, :date_added)
                    '''
        )

        with self._engine.connect() as conn:
            conn.execute(
                stmt,
                dict(
                    file_hash=file_hash,
                    file_path=file_path,
                    date_added=dt.datetime.now(),
                ),
            )
            conn.commit()

    def get_file_paths(self) -> set:
        '''Returns a set of the file paths in the database'''

        stmt = text(
            '''
                    SELECT file_path
                    FROM files
                    '''
        )

        with self._engine.connect() as conn:
            result = conn.execute(stmt)

        return_set = set()

        if result.rowcount:
            for row in result:
                return_set.add(row.file_path)

        return return_set

    def get_file_hashes(self) -> set:
        '''Returns a set of the file hashes in the database'''

        stmt = text(
            '''
                    SELECT file_hash
                    FROM files
                    '''
        )

        with self._engine.connect() as conn:
            result = conn.execute(stmt)

        return_set = set()

        if result.rowcount:
            for row in result:
                return_set.add(row.file_hash)

        return return_set
