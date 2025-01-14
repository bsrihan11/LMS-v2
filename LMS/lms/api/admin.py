from datetime import datetime, timedelta, timezone
from flask import jsonify,request
from lms.forms import AdUpUserForm
from lms.api import api
from lms.api.utils import admin_required
from lms.models import Role, Transaction, User,Author,Section,Rating
from lms import db,cache



@api.route("/admin",methods=['GET'])
@admin_required
def admin():
    section_data =  {}

    for section in Section.query.filter(Section.section_name != 'DEFAULT').all():
        section_data[section.section_name] = section.vol_sold()

    ratings,total_rating = 0,0

    for rating in Rating.query.all():
        ratings+=rating.rating
        total_rating+=1

    avg_rating = 0 if total_rating==0 else ratings/total_rating


    current_datetime = datetime.now(timezone.utc)
    trans_24 = 0
    for trans in Transaction.query.all():
        datetime_24_hours_ago = current_datetime - timedelta(hours=24)
        if datetime_24_hours_ago <= trans.transaction_time.replace(tzinfo=timezone.utc) <= current_datetime:
            trans_24+=1

    sorted_authors = sorted(Author.query.all(),key=lambda x:x.vol_sold(),reverse=True)
    sorted_authors = sorted_authors[:10] if len(sorted_authors)>10 else sorted_authors
    top_authors = [author.author_name for author in sorted_authors]

    roles = []

    for role in Role.query.all():
        dic = {
            'role_id':role.role_id,
            'role_name':role.role_name
        }
        roles.append(dic)
    
    response = jsonify(message = "This is admin page.",admin={'top_authors':top_authors,'avg_rating':avg_rating,
                       "section_data":section_data,"trans_24":trans_24,'roles':roles})
    
    return response,200

@api.route("/admin/get_user",methods=['PUT'])
@admin_required
def get_user():
    data = request.get_json()

    email = data.get('email')

    if email:
        user = User.query.filter_by(email = email).first()
        if user:
            response = jsonify(user={
                'user_id':user.user_id,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'role':user.role_id,
                'active':user.active

            })

            return response,200
        
        else:
            return jsonify(errors={'general':'invalid user.'}), 401

    else:
        return jsonify(errors={'general':'invalid request.'}), 404


@api.route("/admin/update_user",methods=['PUT'])
@admin_required
def update_user():

    data = request.get_json()

    user_id = data.get('user_id')
    active = data.get('active')
    role_id = data.get('role_id')

    print(user_id,role_id,active)
    if user_id and (active == 0 or active ==1) and role_id:

        form = AdUpUserForm(user_id=user_id,active=active,role_id=role_id)

        if form.validate():
            user = User.query.get(user_id)
            if user:
                user.active = active
                user.role_id = role_id
                db.session.commit()
                result = user.to_json()

                if not user.is_active():
                    cache.delete(f'user-{user.user_id}')
                    cache.delete(f'user-{user.user_id}-collection')

                    return jsonify(message={'general':'user updated successfully.'}),200

                cache.set(f"user-{user_id}", result , timeout = 24 * 60 * 60)

                return jsonify(message={'general':'user updated successfully.'}),200
            else:
                return jsonify(errors={'general':'invalid user.'}), 401
        else:

            return  jsonify(errors={'general':'invalid credentials.'}), 401
        
    else:
        return  jsonify(errors={'general':'invalid request.'}), 404
