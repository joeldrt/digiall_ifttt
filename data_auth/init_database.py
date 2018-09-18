from da_ifttt_api import db
from data_auth.models import AuthorityModel, UserModel


def init_database():
    db.create_all()

    if not UserModel.find_by_email('admin@localhost.com'):
        authority1 = AuthorityModel(authority_name='ROLE_ADMIN')
        authority2 = AuthorityModel(authority_name='ROLE_USER')

        db.session.add(authority1)
        db.session.add(authority2)
        db.session.commit()

        admin = UserModel(
            username='admin',
            password=UserModel.generate_hash('admin'),
            firstName='Administrator',
            lastName='Administrator',
            email='admin@localhost.com'
        )

        admin.authorities.append(authority1)
        admin.authorities.append(authority2)

        admin.save_to_db()
