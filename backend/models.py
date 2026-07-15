from database import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    patient_code = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Patient {self.patient_code}>"

class Operator(db.Model):
    __tablename__ = "operators"

    id = db.Column(db.Integer, primary_key=True)

    operator_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Operator {self.operator_code}>"
    
class Center(db.Model):
    __tablename__ = "centers"

    id = db.Column(db.Integer, primary_key=True)

    center_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Center {self.center_code}>"
    
class Study(db.Model):
    __tablename__ = "studies"

    id = db.Column(db.Integer, primary_key=True)

    study_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    study_type = db.Column(
        db.String(50),
        nullable=False
    )

    modality = db.Column(
        db.String(50),
        nullable=False
    )

    study_date = db.Column(
        db.DateTime,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Received"
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    operator_id = db.Column(
        db.Integer,
        db.ForeignKey("operators.id"),
        nullable=False
    )

    center_id = db.Column(
        db.Integer,
        db.ForeignKey("centers.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Study {self.study_code}>"
    
class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    file_type = db.Column(
        db.String(50),
        nullable=False
    )

    file_size = db.Column(
        db.Integer,
        nullable=False
    )

    file_path = db.Column(
        db.String(255),
        nullable=False
    )

    sha256 = db.Column(
        db.String(64),
        nullable=False
    )

    study_id = db.Column(
        db.Integer,
        db.ForeignKey("studies.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<File {self.filename}>"
    
class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)

    report_text = db.Column(
        db.Text,
        nullable=False
    )

    study_id = db.Column(
        db.Integer,
        db.ForeignKey("studies.id"),
        nullable=False,
        unique=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Report {self.id}>"
    
class History(db.Model):
    __tablename__ = "history"

    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(
        db.String(255),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    study_id = db.Column(
        db.Integer,
        db.ForeignKey("studies.id"),
        nullable=True
    )

    def __repr__(self):
        return f"<History {self.action}>"
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    failed_attempts = db.Column(
        db.Integer,
        default=0
    )

    is_locked = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<User {self.username}>"