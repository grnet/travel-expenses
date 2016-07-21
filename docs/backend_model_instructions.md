Introduction
============

The Travel Expenses Backend API exposes all the related info through REST API. [Django REST Framework](http://www.django-rest-framework.org/) (DRF) is used for that purpose. DRF is a powerful and flexible toolkit for building Web APIs.

The standard workflow for creating REST APIs using DRF is the following: 1. Create the **model** to work with. 2. Create a **serializer** class, to provide a way of serializing and deserializing the model instances into representations such as `json`. 3. Create a **viewset** that uses the already defined serializer. 4. Wire the defined viewsets with specific **URLs**.

Each one of the above steps needs to be configured manually with a number of parameters every time a new model is defined. Travel Expenses Backend automates this process by using viewset factories. Viewset factories utilize serializer factories (creating [HyperLinkedModel serializers](http://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer)). This design leads to a more centralized configuration approach. More specifically, all configuration takes place at model definition level.

After model definition, it follows the URL wiring step where for a specific URL, the viewset factory generates the relative viewset with is respective serializer.

Expose a model to REST API
==========================

You can easily create a new model and expose it to REST API by following the steps below.

Model Definition
----------------

First, you have to define your django model with your fields and their constraints:

```python
class MyModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    number = models.FloatField(blank=False)
    another_moddel = models.ForeignKey(AnotherModel)
```

API configuration
-----------------

After specifying your model you have to specify an inner class where you define how your model's fields will be treated by API, e.g. exposed fields, read only fields, filter fields, ordering_fields, etc.

```python
class MyModel(models.Model):
    # Same code as above.

    class APITravel:
        pass
```

You can name the inner class as you wish or you can have multiple inner classes (configurations). In this case you have to declare it at the `api_name` argument of the viewset factory method. The default inner class name is "APITravel".

### Define the fields to expose

In the APITravel inner class define the `fields` attribute. This is a tuple of model field names.

```python
class MyModel(models.Model):
    # Same code as above.

    class APITravel:
        fields = ('id', 'url', 'name', 'number') # Fields exposed to API
```

The fields defined must exist in the model definition. The `url` field is an extra field created by the HyperLinked Model Serializer.

The default value for `fields` attribute is `__all__` which is translated to all fields.

### Read Only Fields

Use the `read_only_fields` attribute to define which fields will be read-only.

```python
class MyModel(models.Model):
    # Same code as above.

    class APITravel:
        fields = ('id', 'url', 'name', 'number') # Fields exposed to API
        read_only_fields = ('id', 'url')
```

The default value for `read_only_fields` attribute is `('url','id')` tuple.

### Filter fields

If all you need is simple equality-based filtering, you can set a filter_fields attribute on the APITravel inner class, listing the set of fields you wish to filter against.

```python
class MyModel(models.Model):
    # Same code as above.

    class APITravel:
        fields = ('id', 'url', 'name', 'number') # Fields exposed to API
        read_only_fields = ('id', 'url')
        filter_fields = ('name','number')
```

### Search fields

For simple single query parameter based searching define the `search_fields` attribute. The `search_fields` attribute should be a list of names of text type fields on the model, such as CharField or TextField.

```python
class MyModel(models.Model):
    # Same code as above.

    class APITravel:
        fields = ('id', 'url', 'name', 'number') # Fields exposed to API
        read_only_fields = ('id', 'url')
        filter_fields = ('name','number')
        search_fields=('name',)
```

### Ordering fields

For simple query parameter controlled ordering of results use `ordering_fields` attribute.

```python
class MyModel(models.Model):
    # Same code as above.

    class APITravel:
        fields = ('id', 'url', 'name', 'number') # Fields exposed to API
        read_only_fields = ('id', 'url')
        filter_fields = ('name','number')
        search_fields=('name',)
        ordering_fields = ('name',)
```

### Allowed Viewset Operations

The default allowed viewset operations are ('list', 'retrieve','create','update','delete'). You can customize this behavior by using the `allowed_operations` attribute.

```python
class MyModel(models.Model):
    # Same code as above.

    class APITravel:
        fields = ('id', 'url', 'name', 'number') # Fields exposed to API
        read_only_fields = ('id', 'url')
        filter_fields = ('name','number')
        search_fields=('name',)
        ordering_fields = ('name',)
        allowed_operations = ('list', 'retrieve', 'delete')
```

### Nested Relations

Nested serialization is also supported. For example, you may want to expose the relations of model to
one single serializer in order to easily read/create/update objects.
All you have to do is to specify the attribute `nested_relations` with a list of tuples of your relations by specifying the name of your nested serializer and the name of the corresponding model field. Our mechanism we will find how the given model is related and will initialize nested serializer accordingly.

However, as the django rest framework supports only read only nested serializers, if you want to
support nested serializer fields you'll need to override `create` and `update` methods of serializer
class.

```python
class MyModel(models.Model):
    # Same code as above.

    class APITravel:
        fields = ('id', 'url', 'name', 'number') # Fields exposed to API
        read_only_fields = ('id', 'url')
        filter_fields = ('name','number')
        search_fields=('name',)
        ordering_fields = ('name',)
        allowed_operations = ('list', 'retrieve', 'delete')
        nested_relations = [('api_field_name', 'another_model')]
```

**Note 1** : If you want to **override the serializer methods** and provide custom implementations for your model then you can simply add your code to a new module with the snake case name of your model inside `serializers` package. Factory function will include them and will override custom implementation.The methods supported are **('create', 'update', 'delete', 'validate')**

**Note 2** : If you want to **override the viewset methods** and provide custom implementations for your model then you can simply add your code to a new module with the snake case name of your model inside `views` package. Factory function will include them and will override custom implementation. The methods supported are **('create', 'update', 'delete')**

**Note 3** :In case, you only want to change the Python behavior of a model – perhaps to change the default manager, or add a new method, use a **Proxy model** that extends the current model. You can create, delete and update instances of the proxy model and all the data will be saved as if you were using the original (non-proxied) model. The following is a proxy model example.

```python
class MyProxyModel(MyModel):
    class Meta:
        proxy = True

    def do_something(self):
        # ...
        pass
```

Finally, register your API endpoint which will perform CRUD operations to your newly created model by adding the following line to your `urls.py` file. It calls a factory function for constructing a viewset and serializer for your model.

```python
router_petition.register(
    r'my_model', viewset_factory(MyModel, YourCustomPermission))
```

**Note** : "YourCustomPermissions" are model level custom permissions. This permissions are placed between the two default permissions: `IsAuthenticated` and `DjangoModelPermissions` classes. So the permissions order is defined like this: 1. IsAuthenticated, 2. YourCustomPermissions, 3. DjangoModelPermissions

Don't forget to perform the required schema migrations after adding your model by running:

```
python manage.py makemigrations texpenses
python manage.py migrate
```
