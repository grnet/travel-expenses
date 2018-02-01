from apimas.drf.permissions import ApimasPermissions
from apimas.documents import doc_to_ns


class NestedPermissions(ApimasPermissions):

    def _is_list_of_dicts(self, value):
        return isinstance(value, list) and all(map(lambda v: isinstance(v, dict), value))
       
    def _resolve_data_fields(self, data):
        common_fields = super(NestedPermissions, self)._resolve_data_fields(data)
        nested_array_fields = []
        for key, val in data.iteritems():
            if self._is_list_of_dicts(val):
                for item in val:
                    nested_array_fields += doc_to_ns({ key: item }).keys()
        common_fields = set(list(common_fields) + nested_array_fields)
        return common_fields
