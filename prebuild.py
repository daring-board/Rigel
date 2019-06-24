import shutil
import subprocess

shutil.copyfile("./model/labels.json", "./rigel/src/assets/labels.json")

cmd = 'tensorflowjs_converter --input_format=keras ./model/custum_resnet.h5 ./rigel/public/model'
returncode = subprocess.call(cmd)