from config import db

# class login(db.model):
#     __tablename__ = "loginPage"
#     email = db.Column(db.String(25), unique=True, nullable=False)
   
class Log(db.Model):
    __tablename__ = "logs"
    log_id = db.Column(db.Integer, primary_key=True)
    brid = db.Column(db.String(15), nullable = True) #Got from login page
    obn = db.Column(db.String(100), nullable = False)
    project_name = db.Column(db.String(100),nullable = False,unique=True) 
    golive_date = db.Column(db.Date, nullable = False)
    deployment_startdate = db.Column(db.Date, nullable = False)
    deployment_enddate = db.Column(db.Date, nullable = False)
    dev_name = db.Column(db.String(100),nullable = False)
    qe_name = db.Column(db.String(100),nullable = False)
    conflict = db.Column(db.Boolean, default = False)

class ImpactedChannel(db.Model):
    __tablename__ = "impacted_channels"
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('logs.log_id'),nullable = False)
    impacted_channel = db.Column(db.String(100), nullable=False, default="Apply")

class ConflictInfo(db.Model):
    __tablename__ = "conflict_info"
    #id = db.Column(db.Integer, primary_key=True) 
    log_id = db.Column(db.Integer, db.ForeignKey('logs.log_id'),primary_key=True, nullable = False,)
    conflict_attachment = db.Column(db.LargeBinary, nullable=True)

class RecordsConflict(db.Model):
    __tablename__ = "records_conflict"
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('logs.log_id'), nullable=False)
    conf_log_id = db.Column(db.Integer, nullable=False)