from rest_framework import serializers

from .models import Comment, Like, Review, User, Movie


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "gender",
            "first_name",
            "last_name",
            "email",
            "avatar",
        )

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
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
    target = LikedObjectField(source="content_object", read_only=True)

    class Meta:
        model = Like
        fields = "__all__"
