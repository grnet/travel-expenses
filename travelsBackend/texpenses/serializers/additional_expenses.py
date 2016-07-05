from texpenses.models import Petition


def create(self, validated_data):
    request = self.context['request']
    petition = str(request.data['petition'])
    petition_id = petition[petition.index('user_petition') + 14:-1]

    petition_object = Petition.objects.get(id=petition_id)
    request.data['user'] = petition_object.user
    validated_data['user'] = request.data['user']
    model_name = getattr(self.Meta, 'model')
    return model_name.objects.create(**validated_data)
