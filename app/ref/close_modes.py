CLOSE_MODES = {
    "MANUAL": "manually closed by user",
    "MANUAL_ADMIN": "manually closed by admin",
    "UNDEFINED": "undefined"
}

REQUESTS_CLOSE_MODES = CLOSE_MODES.copy()
REQUESTS_CLOSE_MODES["ALL_FOUND"] = "all password found"
REQUESTS_CLOSE_MODES["ALL_PERFORMED"] = "all attacks performed"
REQUESTS_CLOSE_MODES["EXPIRED"] = "request duration expired"

CRACKS_CLOSE_MODES = CLOSE_MODES.copy()
CRACKS_CLOSE_MODES["CMD_FINISHED"] = "haschat command finished"
