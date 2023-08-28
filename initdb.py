import parserlib.db.engine
import parserlib.db.model

parserlib.db.model.Base.metadata.create_all(parserlib.db.engine.engine)