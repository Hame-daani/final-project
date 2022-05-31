from rest_framework import serializers

from .models import Comment, FriendRequest, Like, Review, User, Movie

from random import randint


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    similarity = serializers.FloatField(required=False, source="sim")
    pic = serializers.SerializerMethodField()
    gender = serializers.CharField(source="get_gender_display")

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "similarity",
            "password",
            "gender",
            "first_name",
            "last_name",
            "email",
            "pic",
            "date_joined",
        )

    def get_pic(self, obj):
        if obj.gender == "F":
            return f"https://randomuser.me/api/portraits/women/{obj.id%100}.jpg"
        else:
            return f"https://randomuser.me/api/portraits/men/{obj.id%100}.jpg"

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class MovieSerializer(serializers.ModelSerializer):
    similarity = serializers.FloatField(required=False, source="sim")
    friends_er = serializers.FloatField(required=False)
    global_er = serializers.FloatField(required=False)
    avg_rating = serializers.FloatField(required=False)
    imdb_link = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def get_imdb_link(self, obj):
        base = "https://www.imdb.com/"
        return f"{base}/title/tt{int(obj.imdbid):07}"


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class CommentedObjectField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, Review):
            serializer = ReviewSerializer(value)
        elif isinstance(value, Comment):
            serializer = CommentSerializer(value)
        else:
            raise Exception("Unexpected type of tagged object")

        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # target = CommentedObjectField(source="content_object", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        fields["comments"] = CommentSerializer(many=True)
        return fields


class LikedObjectField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, Review):
            serializer = ReviewSerializer(value)
        elif isinstance(value, Comment):
            serializer = CommentSerializer(value)
        else:
            raise Exception("Unexpected type of tagged object")

        return serializer.data


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # target = LikedObjectField(source="content_object", read_only=True)

    class Meta:
        model = Like
        fields = "__all__"


class FrSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = "__all__"
