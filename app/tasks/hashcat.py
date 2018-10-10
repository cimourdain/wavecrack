# local imports
from server import app, celery, db
from app.models.cracks.entity import Crack
from app.models.cracks.request import CrackRequest
from app.helpers.files import FilesHelper


def write_errors(folder, errors):
    FilesHelper.create_new_file(
        file_path=folder,
        file_name="errors.txt",
        content=errors
    )
    return True


#  the bind decorator argument > access to task id
@celery.task(bind=True)
def launch_new_crack_request(self, crack_request_id):

    app.logger.info("celery :: hashcat :: load crack request")
    new_crack_request = CrackRequest.query.filter_by(id=crack_request_id).one()

    if new_crack_request:
        app.logger.debug("celery :: hashcat :: set celery_request_id to "+str(self.request.id))
        new_crack_request.celery_request_id = self.request.id
        db.session.commit()

        app.logger.debug("celery :: hashcat :: run cracks ")
        new_crack_request.run_cracks()
    else:
        app.logger.error("Impossible to find crack request with id "+str(crack_request_id))


@celery.task
def kill_crack(crack_id):
    crack = Crack.query.filter(id=crack_id).one()
    crack.kill_process()
