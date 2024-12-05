class CurrentComment:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["view"].get_current_comment()

    def __repr__(self):
        return "%s()" % self.__class__.__name__
