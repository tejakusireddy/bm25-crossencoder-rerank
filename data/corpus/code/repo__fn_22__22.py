def jsonify_payload(self):
        
        # Assume already json serialized
        if isinstance(self.payload, string_types):
            return self.payload
        return json.dumps(self.payload, cls=StandardJSONEncoder)