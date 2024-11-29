from flask import request, jsonify, session, send_file
from config import app,db
from model import *
from datetime import datetime
import logging
import io
from exceptions import *

 
logger = logging.getLogger(__name__)
session = {}

@app.route("/submit_log", methods=['POST'])
def submit_log():
 
    logger.info("Received details to submit an entry")
 
    data = request.json
    impacted_channels = data.get("impactedChannels",[])
 
    logger.debug(f"Data received : {data}")
    #CE
    req_fields = ['deploymentStartDate','deploymentEndDate','obn','projectName','devName','qeName']
    missing_fields = [field for field in req_fields if field not in data]
    if missing_fields:
        logger.error(f"Field(s) missing : {missing_fields}")
        raise MissingFieldException(missing_fields)
    #CE
 
    try:
     deployment_startdate = datetime.strptime(data['deploymentStartDate'], '%Y-%m-%d').date()
     deployment_enddate = datetime.strptime(data['deploymentEndDate'], '%Y-%m-%d').date()
     goLiveDate=datetime.strptime(data['goLiveDate'], '%Y-%m-%d').date()
    except Exception as e:
        logger.error(f"Error in date format : {e}")
        return jsonify({"error: Invalid date format"}),400
    #CE
    if(deployment_startdate>deployment_enddate):
        raise InvalidDateRangeException
    if(goLiveDate<deployment_enddate):
        raise InvalidGLDateRangeException
    # except InvalidDateRangeException as e:
    #     return jsonify({"error": str(e)}),404
    # else:
    #     InvalidDateRangeException as e:
    #     logger.error(f"Deployment Start date is later Deployment End Date")
    #     return jsonify({"error": str(e)}),404 
    #CE
 
    conflicting_logs = check_Conflicts(deployment_startdate,deployment_enddate,impacted_channels)
   
    if conflicting_logs:
        logger.warning("Conflict detected with existing logs")

        session['cached_log_data'] = data
        session['conflicting_log_ids'] = [log.log_id for log in conflicting_logs]

        conflict_details = [{"developer":log.dev_name,"qe":log.qe_name,"projectName":log.project_name} for log in conflicting_logs]
        return jsonify({"conflict":True,"conflictDetails":conflict_details}), 409
   
    new_log = Log(
        obn = data["obn"],
        project_name = data["projectName"],
        golive_date = datetime.strptime(data["goLiveDate"],'%Y-%m-%d').date(),
        deployment_startdate=deployment_startdate,
        deployment_enddate=deployment_enddate,
        dev_name = data['devName'],
        qe_name = data['qeName'],
        conflict = False
    )
 
    db.session.add(new_log)
    db.session.commit()
    logger.info("New entry added to the DB successfully")
 
    for channel in impacted_channels:
        impacted_channel = ImpactedChannel(log_id = new_log.log_id, impacted_channel=channel)
        db.session.add(impacted_channel)
 
    db.session.commit()
    logger.info("Impacted channels added successfully")
    return jsonify({"message":"Log added successfully"}), 200
 
 
 
@app.route('/resolve_conflict',methods=["POST"])
def resolve_conflict():
 
    logger.info("received request for resolving conflict")
 
    attachment = request.files['conflictAttachment'].read() if 'conflictAttachment' in request.files else None
 
    if attachment is None:
        logger.warning("No attachement is provided!")
        return jsonify({"error": "No attachment provided"}), 400
    # #CE
    # if attachment:
    #     try:
    #         attachment_data=attachment.read()
    #     except Exception: 
    #         raise FileReadException()
    # #CE
   
    cached_data = session.get('cached_log_data')
    if not cached_data:
        logger.error("No cached data found")
        return jsonify({"error": "No cached data found.Try again!!"}), 400
   
    try:
      new_log = Log(
        obn = cached_data['obn'],
        project_name = cached_data['projectName'],
        golive_date = datetime.strptime(cached_data["goLiveDate"],'%Y-%m-%d').date(),
        deployment_startdate = datetime.strptime(cached_data['deploymentStartDate'], '%Y-%m-%d').date(),
        deployment_enddate = datetime.strptime(cached_data['deploymentEndDate'], '%Y-%m-%d').date(),
        dev_name = cached_data['devName'],
        qe_name = cached_data['qeName'],
        conflict = True,
      )
 
      db.session.add(new_log)
      db.session.commit()
      logger.info("new entry created succesfully!")
 
      impacted_channels = cached_data.get('impactedChannels',[])
      for channel in impacted_channels:
        impacted_channel = ImpactedChannel(log_id = new_log.log_id, impacted_channel=channel)
        db.session.add(impacted_channel)
 
      conflict_info = ConflictInfo(log_id=new_log.log_id, conflict_attachment=attachment)
 
      db.session.add(conflict_info)

      conflicting_log_ids = session.get('conflicting_log_ids', [])

      for conf_log_id in conflicting_log_ids:
          record_conflict = RecordsConflict(
              log_id=new_log.log_id,
              conf_log_id=conf_log_id
          )
          db.session.add(record_conflict)

      db.session.commit()
      logger.info(f"conflict attachement saved with log id: {new_log.log_id}")
   
    except Exception as e:
        logger.error(f"error occured : {e}")
        db.session.rollback()
        return jsonify({"error": "an error occured while resolving conflict!"}), 500
    session.pop('cached_log_data', None)
    session.pop('conflicting_log_ids', None)
 
    return jsonify({"message":"Log added with Conflict resolved, new log created and attachement saved!!"}), 200
 
@app.route('/download_attachment/<int:log_id>', methods=['GET'])
def download_attachment(log_id):
    try:
        conflict_info = ConflictInfo.query.filter_by(log_id=log_id).first()
        if not conflict_info or not conflict_info.conflict_attachment:
            logger.warning(f"No attachment found for log ID: {log_id}")
            return jsonify({"error":"No attachment found"}),404
        
        attachment = conflict_info.conflict_attachment
        filename = f"attachment_log_{log_id}.xlsx"

        file_stream = io.BytesIO(attachment)
        file_stream.seek(0)

        return send_file(
            file_stream,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    except Exception as e:
        logger.error(f"Error occured while downloading attachment: {e}")
        return jsonify({"error": "An error occurred while downloading the attachment"}), 500

@app.route('/get_logs', methods=['GET'])
def get_logs():
    try:
        logs = Log.query.all()
        # CE
        if not logs:
            raise NoLogsFoundException()
        # CE     
        logger.info("Retrieved data from all the logs table..")
        logs_data = []
        for log in logs:
            if log.conflict:
                impacted_channels = ImpactedChannel.query.filter_by(log_id=log.log_id).all()
                conflict_info = ConflictInfo.query.filter_by(log_id=log.log_id).first()
                download_link = f"{request.host_url}download_attachment/{log.log_id}"
                log_data = {
                "logId":log.log_id,
                "obn":log.obn, 
                "projectName":log.project_name, 
                "goLiveDate": log.golive_date.strftime('%Y-%m-%d'), 
                "deploymentStartDate": log.deployment_startdate.strftime('%Y-%m-%d'),
                "deploymentEndDate": log.deployment_enddate.strftime('%Y-%m-%d'),
                "devName": log.dev_name,
                "qeName": log.qe_name,
                "conflict": log.conflict,
                "impactedChannels": [channel.impacted_channel for channel in impacted_channels],
                "conflictAttachment": download_link
                }  
                logs_data.append(log_data)
            else:
                impacted_channels = ImpactedChannel.query.filter_by(log_id=log.log_id).all()
                log_data = {

                "logId":log.log_id,
                "obn":log.obn, 
                "projectName":log.project_name, 
                "goLiveDate": log.golive_date.strftime('%Y-%m-%d'), 
                "deploymentStartDate": log.deployment_startdate.strftime('%Y-%m-%d'),
                "deploymentEndDate": log.deployment_enddate.strftime('%Y-%m-%d'),
                "devName": log.dev_name,
                "qeName": log.qe_name,
                "conflict": log.conflict,
                "impactedChannels": [channel.impacted_channel for channel in impacted_channels],
                "conflictAttachment": "No Conflict"
                } 
                logs_data.append(log_data)
        return jsonify({"logs":logs_data}),200
    # except Exception as e:
    #    logger.error(f"Error occured while fetching all logs - {e}")
    #    return jsonify({"error": "Error occured while fetching logs"}), 500
    # CE
    except NoLogsFoundException as e:
        return jsonify({"error": str(e)}),404

    except Exception as e:
       logger.error(f"Error occured while fetching all logs : {str(e)}") 
       raise DatabaseConnectionException() from e 
    #CE 
 
 
# def check_Conflicts(start_date,end_date,impacted_channels):
#     conflicts = Log.query.join(ImpactedChannel, Log.log_id == ImpactedChannel.log_id).filter(
#         ((Log.deployment_startdate <= start_date) & (Log.deployment_enddate >= start_date )) |
#         ((Log.deployment_startdate <= end_date) & (Log.deployment_enddate >= end_date )),
#         ImpactedChannel.impacted_channel.in_(impacted_channels)).all()
#     return conflicts

def check_Conflicts(start_date,end_date,impacted_channels):
    date_conflicts=Log.query.filter(
        ((Log.deployment_startdate <= end_date) & (Log.deployment_enddate >= start_date ))
    ).all()

    if date_conflicts:
        conflicts = Log.query.join(

            ImpactedChannel, Log.log_id ==ImpactedChannel.log_id
        ).filter(
            Log.log_id.in_([log.log_id for log in date_conflicts]),
            ImpactedChannel.impacted_channel.in_(impacted_channels)
        ).all()
        return conflicts
    return []
 
 
@app.route("/cache",methods=['GET'])
def cache_data():
    cached_data = session.get('cached_log_data')
    if cached_data is None:
        return jsonify({"message":"Cache data not found!!"})
    return jsonify({"cachedData":cached_data}),200
 
 
 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
   
    app.run(debug=True)