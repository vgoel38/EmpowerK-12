import sys
path = '/home/vgoel38/EmpowerK-12'
if path not in sys.path:
    sys.path.append(path)
from project import app as application