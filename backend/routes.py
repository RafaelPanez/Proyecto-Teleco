import os
import hashlib
import logging 
from flask import request, jsonify, current_app 
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import check_password_hash
from datetime import datetime
from models import (
    User,
    Patient,
    Operator,
    Center,
    Study,
    File,
    Report,
    History 
)
from database import db


def register_routes(app):

    @app.route("/login", methods=["POST"])
    def login():

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()

        if not user:

            logging.warning(f"Intento de acceso con usuario inexistente: {username}")

            return jsonify({
                "success": False,
                "message": "Usuario no encontrado"
            }), 404
        
        if user.is_locked:

            logging.warning(f"Intento de acceso con usuario bloqueado: {username}")

            return jsonify({
                "success": False,
                "message": "Usuario bloqueado. Contacte al administrador."
            }), 403

        if not check_password_hash(user.password_hash, password):

            user.failed_attempts += 1

            if user.failed_attempts >= 3:
                user.is_locked = True

            db.session.commit()

            logging.warning(f"Intento fallido de inicio de sesión: {username}")

            return jsonify({
                "success": False,
                "message": "Contraseña incorrecta",
                "failed_attempts": user.failed_attempts
            }), 401
        
        user.failed_attempts = 0
        db.session.commit()

        access_token = create_access_token(
            identity=user.username
        )

        logging.info(f"Inicio de sesión exitoso: {username}") 

        return jsonify({
            "success": True,
            "message": "Inicio de sesión exitoso",
            "access_token": access_token
        }), 200
    
    @app.route("/upload", methods=["POST"])
    @jwt_required()
    def upload():

        try: 
            current_user = get_jwt_identity()

            if "file" not in request.files:

                return jsonify({
                    "message": "No se recibió ningún archivo."
                }), 400

            file = request.files["file"]
            patient_id = request.form.get("patient_id")
            patient_name = request.form.get("patient_name") 
            study_code = request.form.get("study_code")
            study_type = request.form.get("study_type")
            center_code = request.form.get("center_code")
            center_name = request.form.get("center_name")
            center_location = request.form.get("center_location")
            operator_code = request.form.get("operator_code")
            operator_name = request.form.get("operator_name")
            report = request.form.get("report")

            required_fields = [
                "patient_id",
                "patient_name",
                "study_code",
                "study_type",
                "center_code",
                "center_name",
                "center_location",
                "operator_code",
                "operator_name",
                "report"
            ]

            for field in required_fields:

                if not request.form.get(field):

                    return jsonify({
                        "message": f"El campo '{field}' es obligatorio."
                    }), 400

            patient = Patient.query.filter_by(
                patient_code=patient_id
            ).first()

            if patient is None:

                patient = Patient(
                    patient_code=patient_id,
                    name=patient_name
                )

                db.session.add(patient)
                db.session.flush()
            
            operator = Operator.query.filter_by(
                operator_code=operator_code
            ).first()

            if operator is None:

                operator = Operator(
                    operator_code=operator_code,
                    name=operator_name
                )

                db.session.add(operator)
                db.session.flush()

            center = Center.query.filter_by(
                center_code=center_code
            ).first()

            if center is None:

                center = Center(
                    center_code=center_code,
                    name=center_name,
                    location=center_location
                )

                db.session.add(center)
                db.session.flush()

            study = Study.query.filter_by(
                study_code=study_code
            ).first()

            if study is None:

                study = Study(
                    study_code=study_code,
                    study_type=study_type,
                    modality=study_type,
                    study_date=datetime.now(),
                    patient_id=patient.id,
                    operator_id=operator.id,
                    center_id=center.id
                )

                db.session.add(study)
                db.session.flush()

            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(filepath)
            file_type = file.content_type
            file_size = os.path.getsize(filepath)

            with open(filepath, "rb") as f:

                sha256 = hashlib.sha256(f.read()).hexdigest()
                
            file_record = File.query.filter_by(
                study_id=study.id
            ).first()

            if file_record is None:

                file_record = File(
                    filename=file.filename,
                    file_type=file_type,
                    file_size=file_size,
                    file_path=filepath,
                    sha256=sha256,
                    study_id=study.id
                )

                db.session.add(file_record)
                db.session.flush()

            report_record = Report.query.filter_by(
                study_id=study.id
            ).first()

            if report_record is None:

                report_record = Report(
                    report_text=report,
                    study_id=study.id
                )

                db.session.add(report_record)
                db.session.flush()

            history = History(

                action=f"Estudio {study.study_code} recibido correctamente",

                study_id=study.id

            )

            db.session.add(history)
            db.session.commit()

            logging.info(
                f"Usuario {current_user} subió el archivo {file.filename} | Estudio: {study.study_code} | Paciente: {patient.patient_code}"
            )

            return jsonify({
                "history_id": history.id,
                "file_id": file_record.id,
                "report_id": report_record.id,
                "filename": file.filename,
                "patient_id": patient_id,
                "study_code": study.study_code,
                "study_type": study_type,
                "sha256": sha256,
                "center_code": center.center_code,
                "center_name": center.name,
                "center_location": center.location,
                "operator_code": operator.operator_code,
                "operator_name": operator.name,
                "report": report
            }), 200
        except Exception as e:
            db.session.rollback()

            logging.error(
                f"Error al recibir estudio: {str(e)}"
            )

            return jsonify({
                "message": "Error interno procesando el estudio",
                "error": str(e)
            }), 500
    
    @app.route("/studies", methods=["GET"])
    @jwt_required()
    def get_studies():

        current_user = get_jwt_identity()

        studies = Study.query.all()

        logging.info(
            f"Usuario {current_user} consultó todos los estudios"
        )

        result = []

        for study in studies:

            patient = Patient.query.get(study.patient_id)
            operator = Operator.query.get(study.operator_id)
            center = Center.query.get(study.center_id)
            file = File.query.filter_by(study_id=study.id).first()
            report = Report.query.filter_by(study_id=study.id).first()

            result.append({

                "patient_id": patient.patient_code,

                "patient_name": patient.name,

                "study_code": study.study_code,

                "study_type": study.study_type,

                "study_date": study.study_date,

                "status": study.status,

                "center": center.name,

                "operator": operator.name,

                "filename": file.filename if file else None,

                "report": report.report_text if report else None

            })

        return jsonify(result), 200
    
    @app.route("/study/<study_code>", methods=["GET"])
    @jwt_required()
    def get_study(study_code):

        current_user = get_jwt_identity()

        study = Study.query.filter_by(
            study_code=study_code
        ).first()

        if study is None:

            return jsonify({
                "message": "Estudio no encontrado."
            }), 404
        
        logging.info(
            f"Usuario {current_user} consultó el estudio {study_code}"
        )

        patient = Patient.query.get(study.patient_id)
        operator = Operator.query.get(study.operator_id)
        center = Center.query.get(study.center_id)
        file = File.query.filter_by(study_id=study.id).first()
        report = Report.query.filter_by(study_id=study.id).first()

        return jsonify({

            "patient_id": patient.patient_code,

            "patient_name": patient.name,

            "study_code": study.study_code,

            "study_type": study.study_type,

            "study_date": study.study_date,

            "status": study.status,

            "center": center.name,

            "operator": operator.name,

            "filename": file.filename if file else None,

            "report": report.report_text if report else None

        }), 200


    @app.route("/study/<study_code>", methods=["DELETE"])
    @jwt_required()
    def delete_study(study_code):
        current_user = get_jwt_identity()
        study = Study.query.filter_by(
            study_code=study_code
        ).first()
        if study is None:
            return jsonify({
                "message": "Estudio no encontrado."
            }), 404

        file_record = File.query.filter_by(
            study_id=study.id
        ).first()
        if file_record:
            try:
                if os.path.exists(file_record.file_path):
                    os.remove(file_record.file_path)
            except Exception as e:
                logging.error(
                    f"Error al eliminar archivo fisico del estudio {study_code}: {str(e)}"
                )
            db.session.delete(file_record)

        report_record = Report.query.filter_by(
            study_id=study.id
        ).first()
        if report_record:
            db.session.delete(report_record)

        History.query.filter_by(
            study_id=study.id
        ).update({"study_id": None})

        db.session.delete(study)

        history = History(
            action=f"Estudio {study_code} eliminado por el usuario {current_user}",
            study_id=None
        )
        db.session.add(history)

        db.session.commit()

        logging.info(
            f"Usuario {current_user} elimino el estudio {study_code}"
        )

        return jsonify({
            "message": "Estudio eliminado correctamente"
        }), 200
