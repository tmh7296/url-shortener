from schema import Schema, And, Use, Optional, SchemaError

def validateRequestBody(shortenedUrl):
    # this module made schema validation a breeze, especially with the ability to provide custom lambdas
    shortenedUrlSchema = Schema({
        'url': And(Use(str), lambda url: 0 < len(url)),
        Optional('slug'): And(Use(str), lambda slug: slug.isalnum() and 0 < len(slug) <= 15)
    })

    try:
        shortenedUrlSchema.validate(shortenedUrl)
        return True
    except SchemaError:
        return False
