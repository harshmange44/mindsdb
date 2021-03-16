# @TODO, replace with arrow later: https://mirai-solutions.ch/news/2020/06/11/apache-arrow-flight-tutorial/
import xmlrpc
import xmlrpc.client
import time
import pickle

from mindsdb.utilities.config import Config
from mindsdb.utilities.log import log

ray_based = False

class ModelInterface():
    def __init__(self):
        self.config = Config()
        for _ in range(10):
            try:
                time.sleep(3)
                self.proxy = xmlrpc.client.ServerProxy("http://localhost:19329/", allow_none=True)
                assert self.proxy.ping()
                return
            except:
                log.info('Wating for native RPC server to start')
        raise Exception('Unable to connect to RPC server')

    def create(self, name):
        self.proxy.create(name)

    def learn(self, name, from_data, to_predict, datasource_id, kwargs={}):
        self.proxy.learn(name, from_data, to_predict, datasource_id, kwargs)

    def predict(self, name, pred_format, when_data=None, kwargs={}):
        bin = self.proxy.predict(name, pred_format, when_data, kwargs)
        return pickle.loads(bin.data)

    def analyse_dataset(self, ds):
        bin = self.proxy.analyse_dataset(ds)
        return pickle.loads(bin.data)

    def get_model_data(self, name, db_fix=True):
        bin = self.proxy.get_model_data(name, db_fix)
        return pickle.loads(bin.data)

    def get_models(self):
        bin = self.proxy.get_models()
        return pickle.loads(bin.data)

    def delete_model(self, name):
        self.proxy.delete_model(name)
