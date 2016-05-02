from iupdsmanager.models import Profile, Application
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = ('uid','user_id_old','email','username','full_name',
                  'first_name','last_name','is_admin','is_active','created_at',
                  'updated_at','last_login','is_cloud_admin','admin_type','appscale_user_id')


class ApplicationSerializer(serializers.Serializer):

    class Meta:
        model = Application
        fields = ('client_id', 'name')


# class CommentSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     content = serializers.CharField(max_length=200)
#     created = serializers.DateTimeField()
#
        # def create(self, validated_data):
        #     return Comment.objects.create(**validated_data)
        #
        # def update(self, instance, validated_data):
        #     instance.email = validated_data.get('email', instance.email)
        #     instance.content = validated_data.get('content', instance.content)
        #     instance.created = validated_data.get('created', instance.created)
        #     instance.save()
        #     return instance
