def convert(attribute="id")
        klass = persistence_class
        object = klass.where(attribute.to_sym => self.send(attribute)).first

        object ||= persistence_class.new

        attributes = self.attributes.select{ |key, value| self.class.serialized_attributes.include?(key.to_s) }

        attributes.delete(:id)

        object.attributes = attributes

        object.save

        self.id = object.id

        object
      end