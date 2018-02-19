# -*- coding: utf-8 -*-
import os
import sys
import threading
from os import path
import nixops.state

_multiprocess_shared_ = True

db_file = '%s/test.nixops' % (path.dirname(__file__))
json_file = '%s/test.json' % (path.dirname(__file__))

def setup():
    state = nixops.state.open(db_file)
    state.db.close()

def destroy(state, uuid):
    depl = state.open_deployment(uuid)
    depl.logger.set_autoresponse("y")
    try:
        depl.clean_backups(keep=0)
    except Exception:
        pass
    try:
        depl.destroy_resources()
    except Exception:
        pass
    depl.delete()
    depl.logger.log("deployment ‘{0}’ destroyed".format(uuid))

def teardown():
    state = nixops.state.open(db_file)
    uuids = state.query_deployments()
    threads = []
    for uuid in uuids:
        threads.append(threading.Thread(target=destroy,args=(state, uuid)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    uuids_left = state.query_deployments()
    state.close()
    if not uuids_left:
        os.remove(db_file)
    else:
        sys.stderr.write("warning: not all deployments have been destroyed; some resources may still exist!\n")
