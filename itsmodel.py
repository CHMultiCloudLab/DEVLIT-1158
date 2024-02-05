from auth import get_api_client

import intersight
import intersight.apis
import intersight.models


def camel_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


class IntersightConnector:
    def __init__(self, api_key, api_key_file, api_endpoint='https://intersight.com'):
        self._client = get_api_client(api_key, api_key_file, api_endpoint)

    def _build_instance_and_object(self, obj_type, obj_param):
        obj_api_name, obj_class_name, *_ = obj_type.split('/')

        # create api_instance
        function_name = obj_api_name.capitalize() + 'Api'
        api_constructor = getattr(intersight.apis, function_name)
        api_instance = api_constructor(self._client)

        # create api_object
        function_name = obj_api_name.capitalize() + obj_class_name[0].upper() + obj_class_name[1:]
        obj_constructor = getattr(intersight.models, function_name)
        api_object = obj_constructor(**obj_param)

        return api_instance, api_object

    def _action_on_instance(self, action, obj_type, _instance, _object, _moid=''):
        obj_api_name, obj_class_name, *_ = obj_type.split('/')

        with self._client as api_client:
            try:
                obj_type = obj_api_name.lower() + '_' + camel_to_snake(obj_class_name)

                if action == 'get':
                    get_function = getattr(_instance, f'get_{obj_type}_list')
                    query_filter = dict(filter=f'Moid eq \'{_moid}\'') if _moid != '' else {}
                    obj_list = get_function(**query_filter)
                elif action == 'create':
                    create_function = getattr(_instance, f'create_{obj_type}')
                    obj_list = create_function(_object)
                elif action == 'update':
                    update_function = getattr(_instance, f'update_{obj_type}')
                    obj_list = update_function(_moid, _object)
                elif action == 'delete':
                    delete_function = getattr(_instance, f'delete_{obj_type}')
                    obj_list = delete_function(_moid)
                else:
                    return None  # not the best way to fail

                return obj_list
            except intersight.ApiException as e:
                print("Exception when calling Intersight api: %s\n" % e)

    def read(self, obj_type, obj_param={}):
        api_instance, api_object = self._build_instance_and_object(obj_type, obj_param)
        return self._action_on_instance('get', obj_type, api_instance, api_object).results

    def create(self, obj_type, obj_param={}):
        api_instance, api_object = self._build_instance_and_object(obj_type, obj_param)
        return self._action_on_instance('create', obj_type, api_instance, api_object)

    def update(self, obj_type, moid, obj_param={}):
        api_instance, api_object = self._build_instance_and_object(obj_type, obj_param)
        return self._action_on_instance('update', obj_type, api_instance, api_object, moid)

    def delete(self, obj_type, moid, obj_param={}):
        api_instance, api_object = self._build_instance_and_object(obj_type, obj_param)
        return self._action_on_instance('delete', obj_type, api_instance, api_object, moid)