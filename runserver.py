import os
from app import app


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    # import newrelic.agent
    # newrelic.agent.initialize('conf/newrelic.ini')
    app.run('0.0.0.0', port=port, debug=False, threaded=False)
    # app.run(port=8000, debug=True, host='0.0.0.0')
    # this can be omitted if using gevent wrapped around gunicorn
