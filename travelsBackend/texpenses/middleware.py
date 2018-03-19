import logging
import traceback


logger = logging.getLogger(__name__)

class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        m = ''.join(traceback.format_exc())
        logger.exception(m)
        return None
