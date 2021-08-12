from dramatiq_dashboard import DashboardApp
from waitress import serve
from flaskr.tess1 import broker


# app to make GUI app of redis on 127.0.0.1.5001. Run redis server and visit url on chrome. Turn off Windows firewall
crapp = DashboardApp(broker=broker, prefix="")
serve(crapp, host='127.0.0.1', port=5001)


