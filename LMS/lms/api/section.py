from flask import jsonify, request
from flask.views import MethodView
from lms.forms import SectionForm, format_errors
from lms.api.utils import manager_required
from lms.helpers import set_sections
from lms.models import Section
from lms import db,cache

  

class SectionResource(MethodView):


    def get(self,section_id):
        type = request.args.get('type')
        if type and type == 'BRIEF':
            section_data = Section.query.get(section_id)
            return jsonify(section=section_data.to_json(type='BRIEF')),200

        section_cache = cache.get(f'section-{section_id}')

        if section_cache:
            return jsonify(section=section_cache),200
        else:
            section = Section.query.get(section_id)

            if section and section.section_name!='DEFAULT':
                section_cache = section.to_json()
                cache.set(f'section={section_id}',section_cache,timeout = 4 * 60 * 60)
                return jsonify(section=section_cache),200
            
            else:
                return jsonify(errors={"general":"invalid section."}),404
        
    
    @manager_required
    def post(self):
        data = request.get_json()

        form = SectionForm(data=data)

        if form.validate():
            new_section = Section(**data)

            db.session.add(new_section)

            db.session.commit()

            set_sections()

            return jsonify(message=f"section created.",section_id=new_section.section_id),200
        else:
            return jsonify(errors=format_errors(form.errors)), 401



    @manager_required
    def put(self,section_id):

        section = Section.query.get(section_id)
        if section:

            data = request.get_json()

            form = SectionForm(data=data)

            if form.validate():
                section.section_name = form.section_name.data
                section.section_cover = form.section_cover.data
            
                db.session.commit()

                set_sections()

                return jsonify(message=f'section updated successfully. ID:{section.section_id}'),200

            else:
                return jsonify(errors=format_errors(form.errors)), 401
        else:
            return jsonify(errors= {"general":"invalid section."}), 404

        
    @manager_required
    def delete(self,section_id):
        section = Section.query.get(section_id)

        if section:
            default = Section.query.filter_by(section_name='DEFAULT').first()
            for book in section.books:
                book.section_id = default.section_id
            db.session.commit()
            db.session.delete(section)
            db.session.commit()

            set_sections()
            return jsonify(message="section deleted successfully."),200
        
        else:
            
            return jsonify(errors={"general":"invalid section."}),404


