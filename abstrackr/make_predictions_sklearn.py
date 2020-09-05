'''
Byron C. Wallace
4/21/2014
'''

import os, pdb, pickle
import datetime
import sys

####
# external dependencies
####

import ConfigParser

import sklearn_predictor
from sklearn_predictor import BaggedUSLearner

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.sql import select
from sqlalchemy.sql import and_, or_

# home-grown
import abstrackr_dataset

configParser = ConfigParser.RawConfigParser()
configFilePath = os.path.normpath(os.path.join(os.path.dirname(__file__), r'../config.txt'))
configParser.read(configFilePath)

engine = create_engine(configParser.get('abstrackr', 'mysql_address'))
conn = engine.connect()
metadata = MetaData(bind=engine)

###
# table binding.
#encoded_status = Table("EncodedStatuses", metadata, autoload=True) # we no longer need this.
prediction_status = Table("predictionstatuses", metadata, autoload=True)
predictions_table = Table("predictions", metadata, autoload=True)
citations = Table("citations", metadata, autoload=True)
priorities = Table("priorities", metadata, autoload=True)
labels = Table("labels", metadata, autoload=True)
reviews = Table("projects", metadata, autoload=True)
users = Table("user", metadata, autoload=True)
labeled_features = Table("labeledfeatures", metadata, autoload=True)
#encoded_status = Table("encodedstatuses", metadata, autoload=True)

def ensure_db_connection(func):
    def test_for_stale_connection(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            engine = create_engine(configParser.get('abstrackr', 'mysql_address'))
            conn = engine.connect()
            metadata = MetaData(bind=engine)

            # bind the tables
            citations = Table("citations", metadata, autoload=True)
            labels = Table("labels", metadata, autoload=True)
            reviews = Table("projects", metadata, autoload=True)
            users = Table("user", metadata, autoload=True)
            labeled_features = Table("labeledfeatures", metadata, autoload=True)
            encoded_status = Table("encodedstatuses", metadata, autoload=True)
            prediction_status = Table("predictionstatuses", metadata, autoload=True)
            predictions = Table("predictions", metadata, autoload=True)
            priorities = Table("priorities", metadata, autoload=True)

            # Actually execute.
            return func(*args, **kwargs)

    return test_for_stale_connection

def make_predictions(review_id):
    #predictions, train_size, num_pos = pred_results
    print "making predictions for review: %s" % review_id
    ids, titles, abstracts, mesh, lbls_dict = get_data_for_review(review_id)
    try:
        review_dataset = abstrackr_dataset.Dataset(ids, titles, abstracts, mesh,
                                                lbls_dict, name=str(review_id))
    except Exception as e:
        print e
        return False

    if review_dataset.is_everything_labeled():
        return False

    learner = BaggedUSLearner(review_dataset)
    print "training..."
    try:
        learner.train()
    except Exception as e:
        return False

    print "ok! making predictions..."
    try:
        pred_d, train_size, num_pos = learner.predict_remaining()
    except Exception as e:
        return False
    print "-"*20 + " summary for review %s " % review_id + "-"*20
    print "training set size: %s\ntest set size: %s\n# predicted to be positive: %s" % (
            train_size, len(pred_d), num_pos)
    print "-"*62
    print "done. updating tables..."

    _update_predictions(review_id, pred_d, train_size, num_pos)
    print "okey dokey.\n"

@ensure_db_connection
def _update_predictions(review_id, predictions, train_size, num_pos):
    ####
    # update the database
    ####

    # first, delete all prediction entries associated with this
    # review (these are presumably 'stale' now)
    conn.execute(
        predictions_table.delete().where(predictions_table.c.project_id == review_id))

    # map -1's to 0's; this is because the ORM (sql-alchemy)
    # expects boolean fields to be either 0 or 1, which is apparently
    # a new thing in later releases (oh, well).
    neg_one_to_0 = lambda x : 0 if x < 0 else x

    # now re-insert them, reflecting the new prediction
    for study_id, pred_d in predictions.items():
        conn.execute(predictions_table.insert().values(study_id=study_id, project_id=review_id, \
                    prediction=neg_one_to_0(pred_d["prediction"]), num_yes_votes=pred_d["num_yes_votes"]),
                    predicted_probability=pred_d["pred_prob"])

    # delete any existing prediction status entries, should they exist
    conn.execute(prediction_status.delete().where(prediction_status.c.project_id == review_id))

    # finally, update the prediction status
    conn.execute(prediction_status.insert().values(project_id=review_id, predictions_exist=True,\
         predictions_last_made=datetime.datetime.now(), train_set_size=train_size,\
         num_pos_train=num_pos))


def get_data_for_review(review_id):
    '''
    ids, titles, abstracts, mesh, lbl_dict
    '''
    lbls_dict = _get_lbl_d_for_review(review_id)
    review_citation_dict = _get_ti_ab_mh(review_id)
    # note the ordering
    ids = sorted(review_citation_dict.keys())
    titles, abstracts, mesh = [], [], []
    for id_ in ids:
        citation_d = review_citation_dict[id_]
        titles.append(citation_d["title"])
        abstracts.append(citation_d["abstract"])
        mesh.append(citation_d["keywords"])
    return ids, titles, abstracts, mesh, lbls_dict

@ensure_db_connection
def _get_ti_ab_mh(review_id):
    fields = ["title", "abstract", "keywords"]
    none_to_text= lambda x: "none" if x is None else x

    s = citations.select(citations.c.project_id==review_id)
    citations_for_review = list(s.execute())
    cit_d = {}
    for citation in citations_for_review:
        citation_id = citation['id']
        cit_d[citation_id] = {}
        for field in fields:
            cit_d[citation_id][field] = citation[field]
    return cit_d

@ensure_db_connection
def _get_lbl_d_for_review(review_id):
    lbl_d = {}
    s = labels.select(labels.c.project_id==review_id)
    for lbl in s.execute():
        lbl_d[lbl["study_id"]]=lbl["label"]
    return lbl_d
