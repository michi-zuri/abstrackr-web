'''
Byron C. Wallace
4/21/2014
'''

# standard library imports
import datetime, os, pdb, pickle, random, sys, time
from operator import itemgetter
from builtins import range

# third-party package dependencies
from configparser import RawConfigParser
from sqlalchemy import create_engine, pool, sql, MetaData, Table

# local modules
from . import abstrackr_dataset
from .sklearn_predictor import BaggedUSLearner

################################################################################

config = RawConfigParser()
config.read(os.path.normpath(os.path.join(os.path.dirname(__file__), r'../config.txt')))

def make_predictions(review_id, t_citations, t_labels, t_prediction_status, t_predictions):
    #predictions, train_size, num_pos = pred_results
    print( "making predictions for review # %s" % review_id )
    ids, titles, abstracts, mesh, lbls_dict = get_data_for_review(review_id, t_citations, t_labels)
    try:
        review_dataset = abstrackr_dataset.Dataset(
            ids, titles, abstracts, mesh, lbls_dict, name=str(review_id)
        )
    except Exception as e:
        print( "Exception for Dataset: %s" % e )
        return False

#    skip predictions for finished reviews
#    if review_dataset.is_everything_labeled():
#        return False

    learner = BaggedUSLearner(review_dataset)
    print( "training..." )
    try:
        learner.train()
    except Exception as e:
        print( "Exception for learner.train(): %s" % e )
        return False
    print( "ok! making predictions..." )
    try:
        pred_d, train_size, num_pos = learner.predict_remaining()
    except Exception as e:
        print( "Exception for learner.predict_meaning(): %s" % e )
        return False
    print( "-"*20 + " summary for review %s " % review_id + "-"*20 )
    print( "training set size: %s\ntest set size: %s\n# predicted to be positive: %s"
        %   (                  train_size,        len(pred_d),                    num_pos)
    )
    print( "-"*62 )

    okey_dokey = _update_predictions(review_id, pred_d, train_size, num_pos, t_prediction_status, t_predictions)
    print( "predictions made are %s \n" % okey_dokey )
    return okey_dokey

def _update_predictions(review_id, pred_d, train_size, num_pos, t_prediction_status, t_predictions):
    try:
        print( "done. updating tables..." )
        # first, delete all prediction entries associated with this
        # review (these are presumably 'stale' now)
        t_predictions.delete().where(t_predictions.c.project_id == review_id).execute()

        # map -1's to 0's; this is because the ORM (sql-alchemy)
        # expects boolean fields to be either 0 or 1, which is apparently
        # a new thing in later releases (oh, well).
        neg_one_to_0 = lambda x : 0 if x < 0 else x

        # now re-insert them, reflecting the new prediction
        for study_id, pred in pred_d.items():
            t_predictions.insert().values(study_id=study_id, project_id=review_id, \
                prediction=neg_one_to_0(pred["prediction"]), num_yes_votes=pred["num_yes_votes"]
            ).execute(predicted_probability=pred["pred_prob"])

        # delete any existing prediction status entries, should they exist
        t_prediction_status.delete().where(t_prediction_status.c.project_id == review_id).execute()

        # finally, update the prediction status
        t_prediction_status.insert().values(project_id=review_id, predictions_exist=True,\
             predictions_last_made=datetime.datetime.now()
        ).execute( train_set_size=train_size, num_pos_train=num_pos )

    except Exception as e:
        print( "Update predictions error: %s" % e )
        return False

    return True

def get_data_for_review(review_id, t_citations, t_labels):
    '''
    ids, titles, abstracts, mesh, lbl_dict
    '''
    lbls_dict = _get_lbl_d_for_review(review_id, t_labels)
    review_citation_dict = _get_ti_ab_mh(review_id, t_citations)
    # note the ordering
    ids = sorted(review_citation_dict.keys())
    titles, abstracts, mesh = [], [], []
    for id_ in ids:
        citation_d = review_citation_dict[id_]
        titles.append(citation_d["title"])
        abstracts.append(citation_d["abstract"])
        mesh.append(citation_d["keywords"])
    return ids, titles, abstracts, mesh, lbls_dict

def _get_ti_ab_mh(review_id, t_citations):
    fields = ["title", "abstract", "keywords"]
    none_to_text= lambda x: "" if x is None else x

    s = t_citations.select(t_citations.c.project_id==review_id)
    citations_for_review = list(s.execute())
    cit_d = {}
    for citation in citations_for_review:
        citation_id = citation['id']
        cit_d[citation_id] = {}
        for field in fields:
            cit_d[citation_id][field] = none_to_text( citation[field] )
    return cit_d

def _get_lbl_d_for_review(review_id, t_labels):
    lbl_d = {}
    s = t_labels.select(t_labels.c.project_id==review_id)
    for lbl in s.execute():
        lbl_d[lbl["study_id"]]=lbl["label"]
    return lbl_d

def get_ids_from_names(review_names, t_reviews):
    s = t_reviews.select(t_reviews.c.name.in_(review_names))
    return [review.id for review in s.execute()]

def _all_review_ids(t_reviews):
    return [review.id for review in t_reviews.select().execute()]

def _get_citations_for_review(review_id, t_citations):
    citation_ids = list(sql.select(
        [t_citations.c.id], t_citations.c.project_id == review_id
    ).execute())
    return citation_ids

def _predictions_last_updated(review_id, t_prediction_status):
    if not _do_predictions_exist_for_review(review_id, t_prediction_status):
        return False

    pred_last = list(sql.select(
                    [t_prediction_status.c.predictions_last_made],
                        t_prediction_status.c.project_id == review_id).execute().fetchone())[0]
    return pred_last

def _do_predictions_exist_for_review(review_id, t_prediction_status):
    pred_status = sql.select(
                    [t_prediction_status.c.project_id, t_prediction_status.c.predictions_exist],
                     t_prediction_status.c.project_id == review_id).execute().fetchone()

    if pred_status is None or not pred_status.predictions_exist:
        return False
    return True

def _get_predictions_for_review(review_id, t_predictions):
    '''
    map citation ids to predictions
    '''
    preds = list(sql.select([t_predictions.c.study_id, t_predictions.c.predicted_probability],
                    t_predictions.c.project_id == review_id).execute())
    preds_d = {}
    for study_id, prob in preds:
        preds_d[study_id] = prob
    return preds_d

def _re_prioritize(review_id, sort_by_str, t_citations, t_priorities, t_prediction_status):
    citation_ids = [cit.id for cit in _get_citations_for_review(review_id, t_citations)]
    predictions_for_review = None
    if _do_predictions_exist_for_review(review_id, t_prediction_status):
        # this will be a dictionary mapping citation ids to
        # the number of yes votes for them
        predictions_for_review = _get_predictions_for_review(review_id, t_predictions)
    else:
        # then we have to sort randomly, since we haven't any predictions
        sort_by_str = "Random"

    # we'll map citation ids to the newly decided priorities;
    # these will depend on the sort_by_str
    cit_id_to_new_priority = {}
    if sort_by_str == "Random":
        ordering = list(range(len(citation_ids)))
        # shuffle
        random.shuffle(ordering)
        cit_id_to_new_priority = dict(zip(citation_ids, ordering))
    elif sort_by_str == "Most likely to be relevant":
        # sort the citations by ascending likelihood of relevance
        cits_to_preds = {}
        # first insert entries for *all* citations, set this to 11
        # to prioritize newly added citations (don't want to accidently
        # de-prioritize highly relevant citations). this will take care
        # of any citations without predictions --
        # e.g., a review may have been merged (?) -- citations for which
        # we have predictions will simply be overwritten, below
        for citation_id in citation_ids:
            #cits_to_preds[citation_id] = 11
            cits_to_preds[citation_id] = 1.0

        for study_id, prob in predictions_for_review.items():
            cits_to_preds[study_id] = prob

        # now we will sort by *descending* order; those with the most yes-votes first
        sorted_cit_ids = sorted(cits_to_preds.iteritems(), key=itemgetter(1), reverse=True)

        # now just assign priorities that reflect the ordering w.r.t. the predictions
        for i, cit in enumerate(sorted_cit_ids):
            cit_id_to_new_priority[cit[0]] = i

    #####
    #   TODO -- ambiguous case (i.e., uncertainty sampling)
    ###

    ####
    # now update the priority table for the entries
    # corresponding to this review to reflect
    # the new priorities (above)
    priority_ids_for_review = list(sql.select(
        [t_priorities.c.id, t_priorities.c.citation_id], t_priorities.c.project_id == review_id
    ).execute())
    for priority_id, citation_id in priority_ids_for_review:
        if citation_id in cit_id_to_new_priority:
            priority_update = t_priorities.update(t_priorities.c.id == priority_id)
            priority_update.execute(priority = cit_id_to_new_priority[citation_id])

def _priority_q_is_empty(review_id, t_priorities):
    return len(sql.select([t_priorities.c.id], t_priorities.c.project_id == review_id).execute().fetchall()) == 0

def main():
    # database connection setup with sqlalchemy
    engine = create_engine(config.get('abstrackr', 'mysql_address'), poolclass=pool.NullPool)
    metadata = MetaData(engine)

    # bind the tables
    t_citations = Table("citations", metadata, autoload=True)
    t_labels = Table("labels", metadata, autoload=True)
    t_reviews = Table("projects", metadata, autoload=True)
    t_prediction_status = Table("predictionstatuses", metadata, autoload=True)
    t_predictions = Table("predictions", metadata, autoload=True)
    t_priorities = Table("priorities", metadata, autoload=True)
    #t_users = Table("user", metadata, autoload=True)
    #t_labeled_features = Table("labeledfeatures", metadata, autoload=True)
    #encoded_status = Table("encodedstatuses", metadata, autoload=True) # not used anymore

    # only build models if we have >= MIN_TRAINING_EXAMPLES labels
    MIN_TRAINING_EXAMPLES = 100
    all_reviews = _all_review_ids(t_reviews)
    reviews_to_update = [r for r in all_reviews if not _priority_q_is_empty(r, t_priorities)]

    for review_id in reviews_to_update:
        print( "checking review %s..." % review_id )
        predictions_last_updated = _predictions_last_updated(review_id, t_prediction_status)
        print( "predictions last updated %s" % predictions_last_updated)
        sort_by_str = sql.select([t_reviews.c.sort_by], t_reviews.c.id == review_id).execute()
        if sort_by_str.rowcount == 0:
            print( "Skipping empty review %s -- it doesn't appear to have any articles" % review_id )
            continue
        sort_by_str = sort_by_str.fetchone().sort_by
        labels_for_review = sql.select([t_labels.c.label_last_updated],
		         t_labels.c.project_id==review_id).order_by(t_labels.c.label_last_updated.desc()).execute()
        if labels_for_review.rowcount >= MIN_TRAINING_EXAMPLES:
            most_recent_label = labels_for_review.fetchone().label_last_updated
            print( "the most recent label for review %s is dated: %s" % (review_id, most_recent_label) )
            if not _do_predictions_exist_for_review(review_id, t_prediction_status) or (most_recent_label > predictions_last_updated):
                # make predictions for updated and new reviews.
                if make_predictions(review_id, t_citations, t_labels, t_prediction_status, t_predictions):
                    # now re-prioritize
                    print( "re-prioritizing..." )
                    _re_prioritize(review_id, sort_by_str, t_citations, t_priorities, t_prediction_status)
            else:
                # initial set of predictions
                print( "not updating predictions for %s" % review_id )
        else:
            print( "Skipping review %s : At least %s articles need to be sorted before Abstrackr can make predictions"
                %   (               review_id,    MIN_TRAINING_EXAMPLES)
            )

    print( "done." )

if __name__ == "__main__":
    main()
