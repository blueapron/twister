class JsonApiConverter:
    def __init__(self, input):
        self.input = input

    def convert(self):
        for key in self.input:
            return self.convert_json(key, self.input[key])

    def convert_json(self, name, obj):
        self.result = self.object_identifier(name + 's', obj['id'])

        attributes = {}
        relationships = {}

        for k, v in obj.items():
          if isinstance(v, dict) or isinstance(v, list):
            relationships[k] = v
          else:
            self.add_attribute(attributes, k, v)

        self.result['attributes'] = attributes
        self.parse_relationships(relationships)

        return self.result

    def parse_relationships(self, relationships):
        metadata = {}
        data = []

        for key, value in relationships.items():
            if isinstance(value, dict):
                identifier = self.object_identifier(key + 's', value['id'])
                data.append(self.parse(key + 's', value))
            else:
                identifier = []
                for obj in value:
                    identifier.append(self.object_identifier(key, obj['id']))
                    data.append(self.parse(key, obj))

            metadata[key] = {'data': identifier}

        self.result['relationships'] = metadata
        self.result['included'] = data

    def parse(self, name, obj):
        data = self.object_identifier(name, obj["id"])
        attributes = {}

        for key, value in obj.items():
            self.add_attribute(attributes, key, value)

        data['attributes'] = attributes
        return data

    def add_attribute(self, hash, key, value):
        if key != 'id' and key != 'type':
            hash[key] = value

    def object_identifier(self, type_name, id):
        return {'id': id, 'type': type_name}
