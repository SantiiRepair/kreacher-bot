import sqlalchemy as db

Groups = db.Table(
        "Groups",
        _metadata,
        db.Column("id", db.Integer(), primary_key=True),
        db.Column("chat_id", db.String(255), nullable=False),
        db.Column("Major", db.String(255), default="Math"),
        db.Column("Pass", db.Boolean(), default=True),
)
