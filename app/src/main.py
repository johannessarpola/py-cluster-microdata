import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from sklearn.externals import joblib
import numpy as np
import time
from collections import defaultdict, OrderedDict, Counter
from app.src import input_output, logger_factory, models

log_factory = logger_factory.LoggerFactory()
app_logger = log_factory.instance(__name__)

def main(contexts_f, output_f):
    import os.path
    contexts_folder = contexts_f
    output_folder = output_f

    contexts_filenames = input_output.get_filepaths_in_folder(contexts_f)
    for ctx_fname in contexts_filenames:
        app_logger.info(f'Loading context from {ctx_fname}')
        with open(ctx_fname, 'rb') as ctx_b:
            ctx = joblib.load(ctx_b)
            vectorizer = ctx.vectorizer
            km = ctx.cluster_model
            order_centroids = km.cluster_centers_.argsort()[:, ::-1]
            terms = vectorizer.get_feature_names()
            for i in range(km.n_clusters):
                print("Cluster %d:" % i, end='')
                termsStrs = []
                for ind in order_centroids[i, :10]:
                    termsStrs.append(terms[ind])
                print(f'Top terms: {",".join(termsStrs)}')
            print("Aa")
    pool = ThreadPoolExecutor(max_workers=4)


# TODO Output
#    input_output.write_and_close(output_file, json_str)

if __name__ == "__main__":
    main(".data/test_data/contexts", ".data/test_data/contexts")