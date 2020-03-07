from datetime import datetime
from portal import db

"""
class Diagram {
  int id
  String script
  String name
  String type
  String image
  DateTime createTime
  DateTime updateTime
}
"""
diagram_tag_table = db.Table()


class Diagram(db.Model):
    __tablename__ = 'diagram'
    diagram_id = db.Column(db.Integer, primary_key=True)
    diagram_name = db.Column(db.String(256), unique=True)
    diagram_type = db.Column(db.String)

    diagram_script = db.Column(db.Text)

    script_path = db.Column(db.String)
    image_path = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Diagram diagram_name={}, diagram_script={}, image_path={}".format(
                                                self.diagram_name,
                                                self.diagram_script,
                                                self.image_path)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True)

    @staticmethod
    def insert_tags():
        default_tags = ['diagram', 'uml', 'flow_chat']
        for strTag in default_tags:
            tag = Tag(name=strTag)
            db.session.add(tag)
        db.session.commit()