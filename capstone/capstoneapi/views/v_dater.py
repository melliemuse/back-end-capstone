from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstoneapi.models import Dater


class DaterSerializer(serializers.HyperlinkedModelSerializer):
    """ JSON serializer for dater

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Dater
        url = serializers.HyperlinkedIdentityField(
            view_name='dater',
            lookup_field='id',
        )
        fields = ('id', 'user_id', 'attachment_style', 'location', 'bio',
                  'gender', 'gender_preference', 'kids', 'smoker',
                  'looking_for', 'interests', 'profile_pic', 'age',
                  'age_range', 'tagline', 'been_reported')

        # depth = 2

class Daters(ViewSet):
    
    def retrieve(self, request, pk=None):
        """
        Handles single GET request for Dater

        Returns:
            Response -- JSON serialized Dater Instance
        """

        try:
            dater = Dater.objects.get(pk=pk)
            serializer = DaterSerializer(
            dater, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handles GET request for Dater list

        Returns:
            Response -- JSON list of serialized Dater list
        """
        
        dater = Dater.objects.filter(id=request.auth.user.dater.id)
        

        serializer = DaterSerializer(
        dater, many=True, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Handles DELETE request to Dater resource

        Returns:
            Response -- JSON serialized detail of deleted Dater
        """

        try:
            dater = Dater.objects.get(pk=pk)
            dater.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Dater.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """
        Handles PUT request for individual Dater item

        Returns:
            Response -- Empty body with 204 status code
        """

        dater = Dater.objects.get(pk=pk)
        
        dater.location = request.data["location"]
        dater.bio = request.data["bio"]
        dater.attachment_style_id = request.data["attachment_style_id"]
        dater.gender = request.data["gender"]
        dater.gender_preference = request.data["gender_preference"]
        dater.looking_for = request.data["looking_for"]
        dater.interests = request.data["interests"]
        dater.kids = request.data["kids"]
        dater.smoker = request.data["smoker"]
        dater.profile_pic = request.data["profile_pic"]
        dater.age = request.data["age"]
        dater.age_range = request.data["age_range"]
        dater.tagline = request.data["tagline"]
        dater.been_reported = request.data["been_reported"]

        dater.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

