import cv2, json, os
import numpy as np
from keras.models import Sequential, load_model
from keras.models import Model
from finetuning import CustumModel
import umap
import matplotlib.pyplot as plt

def preprocess(f_list):
    data = []
    for f_path in f_list:
        print(f_path)
        img = cv2.imread(f_path)
        img = cv2.resize(img, (224, 224))
        img = img.astype(np.float32) / 255.0
        data.append(img)
    data = np.asarray(data)
    return data

if __name__ == "__main__":
    base_model = load_model('./model/custum_model.h5')

    extractor = Model(
        inputs=base_model.input,
        outputs=base_model.get_layer("dense_2").output
    )
    extractor.summary()

    base_path = './train/'
    f_list = []
    label = []
    count = 0
    for d in os.listdir(base_path):
        t_list = os.listdir(base_path+d)
        t_list = [base_path+d+'/'+f for f in t_list]
        f_list.extend(t_list)
        t = [count for _ in range(len(t_list))]
        label.extend(t)
        count += 1
    print(label)
    X = preprocess(f_list)
    y = extractor.predict(X)
    
    reducer = umap.UMAP(n_components=2, n_neighbors=5)
    features = reducer.fit_transform(y)

    # colors = ["red", "green", "blue", "orange", "salmon", "yellow", "yellowgreen", "purple", "black", "grey", "aqua"]
    # for idx in range(len(features)):
    #     plt.scatter(features[idx, 0], features[idx, 1], c=colors[label[idx]])
    # plt.show()

    # target = './upload/36ad1e129fa69e444b28963329e3862c--cosplay-video-video-games.jpg'
    target_path = './transfar/datasets/chunli/trainB/'
    for fi in os.listdir(target_path):
        target = target_path+fi
        data = preprocess([target])
        target_y = extractor.predict(data)
        target_f = reducer.transform(target_y)[0]

        nearest = [9999, [], 99, 9999]
        for idx in range(len(features)):
            vec = features[idx]
            dist = np.linalg.norm(vec-target_f)
            if dist < nearest[3]:
                nearest[0] = f_list[idx]
                nearest[1] = vec
                nearest[2] = label[idx]
                nearest[3] = dist
        print(nearest)
