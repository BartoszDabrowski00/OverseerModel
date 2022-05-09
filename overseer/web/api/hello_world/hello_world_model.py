from flask_restx import fields, Namespace

hello_world_namespace = Namespace('Hello World', description='example namespace')

model = hello_world_namespace.model('Greeting', {
    'msg': fields.String(readonly=True, description='Name to say hello to')
})
