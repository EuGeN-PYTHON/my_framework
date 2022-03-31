class ParamRequster:

    @staticmethod
    def get_dict(data):
        dict = {}
        data = data.split('&')
        for i in data:
            k, val = i.split('=')
            dict[k] = val
        return dict

    @staticmethod
    def get_param(env):
        param = env['QUERY_STRING']
        if param:
            param = ParamRequster.get_dict(param)
        return param

    @staticmethod
    def get_data_from_wsgi(env):
        len_data = env.get('CONTENT_LENGTH')
        if len_data:
            len_data = int(len_data)
        else:
            len_data = 0
        if len_data > 0:
            data = env['wsgi.input'].read(len_data)
        else:
            data = b''
        return data

    def parse_data_to_str(self, bite):
        result = {}
        if bite:
            str = bite.decode(encoding='utf-8')
            result = self.get_dict(str)
        return result

    def get_post_params(self, env):
        data = self.get_data_from_wsgi(env)
        data = self.parse_data_to_str(data)
        return data
