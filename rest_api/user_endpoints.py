from flask_restful import Resource, reqparse
from data_auth.models import UserModel, AuthorityModel
from flask_jwt_extended import (create_access_token,
                                jwt_required,
                                get_jwt_identity, get_jwt_claims)

import datetime

user_registration_parser = reqparse.RequestParser(bundle_errors=True)
user_registration_parser.add_argument('username')
user_registration_parser.add_argument('password', required=True)
user_registration_parser.add_argument('firstName', required=True)
user_registration_parser.add_argument('lastName')
user_registration_parser.add_argument('email', required=True)
user_registration_parser.add_argument('authorities', action='append')
user_registration_parser.add_argument('old_password')


class UserRegistration(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()

        if 'ROLE_ADMIN' not in claims['authorities']:
            return {'message': 'You dont have permision to perform this operation'}, 401

        data = user_registration_parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {'message': 'User {} already exists'.format(data['email'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']),
            firstName=data['firstName'],
            lastName=data['lastName'],
            email=data['email']
        )

        for authority in data['authorities']:
            new_user_authority = AuthorityModel.find_by_authority_name(authority)
            if new_user_authority:
                new_user.authorities.append(new_user_authority)

        try:
            new_user.save_to_db()

            return {'message': 'User {} was create'.format(new_user.email)}
        except:
            return {'message': 'Something went wrong'}, 500


user_login_parser = reqparse.RequestParser(bundle_errors=True)
user_login_parser.add_argument('password', required=True)
user_login_parser.add_argument('email', required=True)


class UserLogin(Resource):
    def post(self):
        data = user_login_parser.parse_args()
        current_user = UserModel.find_by_email(data['email'])
        if not current_user:
            return {'message': 'User con email: {} No existe!'.format(data['email'])}, 401

        if UserModel.verify_hash(data['password'], current_user.password):
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=current_user, expires_delta=expires)
            return {
                'id_token': access_token
            }
        else:
            return {'message': 'credenciales incorrectas!'}, 401


class Account(Resource):
    @jwt_required
    def get(self):
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)
        if not current_user:
            return {'message': 'User {} doesnt exists'.format(email)}, 401
        else:
            ret_user = {
                'username': current_user.username,
                'firstName': current_user.firstName,
                'lastName': current_user.lastName,
                'email': current_user.email,
                'authorities': [authority.authority_name for authority in current_user.authorities]
            }
            return ret_user

    @jwt_required
    def put(self):
        data = parser.parse_args()
        user_to_edit = UserModel.find_by_email(data['email'])
        if not user_to_edit:
            return {'message': 'User {} doesnt exists'.format(data['email'])}
        else:
            user_to_edit.firstName = data['firstName']
            user_to_edit.lastName = data['lastName']
            try:
                user_to_edit.save_to_db()

                return {'message': 'User {} was edited'.format(user_to_edit.login)}
            except:
                return {'message': 'Something went wrong'}, 500
