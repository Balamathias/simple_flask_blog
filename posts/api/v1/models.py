'''Model for API endpoints'''

from posts import marsh_mallow as ma
from posts.models import Post, User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    picture = ma.auto_field()
    posts = ma.auto_field()


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True

    author = ma.HyperlinkRelated('user')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

posts_schema = PostSchema(many=True)
post_schema = PostSchema()
