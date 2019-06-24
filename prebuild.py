import shutil, os
import subprocess

shutil.copyfile("./model/labels.json", "./rigel/src/assets/labels.json")

dist_path = './rigel/public/model'

if os.path.exists(dist_path):
    shutil.rmtree(dist_path)

cmd = 'tensorflowjs_converter --input_format=keras ./model/custum_model.h5 '+dist_path
returncode = subprocess.call(cmd)