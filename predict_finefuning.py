import numpy as np
import img_processing as iproc
from keras.models import load_model
from keras.models import Model
import pickle
import umap

if __name__=="__main__":

    '''
    モデルのロード
    '''
    base_model = load_model('./model/custum_model.h5')
    base_model.summary()
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('dense_1').output)

    '''
    画像のロード
    '''
    x, y, label = iproc.load_labeled_imgs('./train/')
    x = np.asarray(x)

    data, f_list = iproc.process('./transfar/cgan/chunli/trainB/', switch=True)
    data = np.asarray(data)

    '''
    推論
    '''
    predict = model.predict(x)
    reducer = umap.UMAP(
        n_components=100,
        n_neighbors=75,
        random_state=0
    )
    reducer.fit(predict)
    predict = model.predict(data)
    predict = reducer.transform(predict)

    '''
    保存
    '''
    ret = {f_list[idx]: predict[idx] for idx in range(len(predict))}
    with open('./transfar/output/trainB_featvec.pkl', 'wb') as f:
        pickle.dump(ret, f)

