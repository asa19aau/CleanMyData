from .choices import valid_extensions


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    extensions = valid_extensions
    if not ext.lower() in extensions:
        raise ValidationError('Unsupported file extension.')