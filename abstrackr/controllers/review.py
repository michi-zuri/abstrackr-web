import pdb
import os
import shutil
import datetime
import random
import re
import time
from operator import itemgetter
import csv
import random
import string

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
import logging
from repoze.what.predicates import not_anonymous, has_permission
from repoze.what.plugins.pylonshq import ActionProtector
from abstrackr.lib.base import BaseController, render
import abstrackr.model as model
from abstrackr.lib import xml_to_sql
from sqlalchemy import or_, and_, desc
from abstrackr.lib.helpers import literal

import pygooglechart
from pygooglechart import PieChart3D, StackedHorizontalBarChart, StackedVerticalBarChart
from pygooglechart import Axis

# this is the path where uploaded databases will be written to
permanent_store = "/uploads/"

log = logging.getLogger(__name__)

### for term highlighting
NEG_C = "#7E2217"
STRONG_NEG_C = "#FF0000"
POS_C = "#4CC417"
STRONG_POS_C = "#347235"
COLOR_D = {1:POS_C, 2:STRONG_POS_C, -1:NEG_C, -2:STRONG_NEG_C}

class ReviewController(BaseController):

    @ActionProtector(not_anonymous())
    def create_new_review(self):
        return render("/reviews/new.mako")
    
    @ActionProtector(not_anonymous())
    def create_review_handler(self):
        # first upload the xml file
        xml_file = request.params['db']
        local_file_path = "." + os.path.join(permanent_store, 
                          xml_file.filename.lstrip(os.sep))
        local_file = open(local_file_path, 'w')
        shutil.copyfileobj(xml_file.file, local_file)
        xml_file.file.close()
        local_file.close()
        
        current_user = request.environ.get('repoze.who.identity')['user']
        new_review = model.Review()
        new_review.name = request.params['name']
        
        # we generate a random code for joining this review
        make_code = lambda N: ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
        review_q = model.meta.Session.query(model.Review)
        existing_codes = [review.code for review in review_q.all()]
        code_length=10
        cur_code = make_code(code_length)
        while cur_code in existing_codes:
            cur_code = make_code(code_length)
        new_review.code = cur_code
        
        new_review.project_lead_id = current_user.id
        new_review.project_description = request.params['description']
        new_review.date_created = datetime.datetime.now()
        new_review.sort_by = request.params['order']
        screening_mode_str = request.params['screen_mode']
        new_review.screening_mode = \
                 {"Single-screen":"single", "Double-screen":"double", "Advanced":"advanced"}[screening_mode_str]
        new_review.initial_round_size = int(request.params['init_size'])
        model.Session.add(new_review)
        model.Session.commit()
        
        # now parse the uploaded file
        if xml_file.filename.endswith(".xml"):
            print "parsing uploaded xml..."
            xml_to_sql.xml_to_sql(local_file_path, new_review)
        else:
            print "assuming this is a list of pubmed ids"
            xml_to_sql.pmid_list_to_sql(local_file_path, new_review)
        print "done."
        
        if new_review.initial_round_size > 0:
            init_ids = self._create_initial_assignment_for_review(new_review.review_id, new_review.initial_round_size)
            # need to remove the initial ids from the priority queue.
            
        # join the person administrating the review to the review.
        self._join_review(new_review.review_id)
        
        c.review = new_review
        return render("/reviews/review_created.mako")
        
    @ActionProtector(not_anonymous())
    def join_a_review(self):
        review_q = model.meta.Session.query(model.Review)
        c.all_reviews = review_q.all()
        return render("/reviews/join_a_review.mako")
        
    @ActionProtector(not_anonymous())
    def join(self, review_code):
        user_id = request.environ.get('repoze.who.identity')['user']
        review_q = model.meta.Session.query(model.Review)
        review_to_join = review_q.filter(model.Review.code==review_code).one()
        redirect(url(controller="review", action="join_review", id=review_to_join.review_id))
        
    @ActionProtector(not_anonymous())
    def join_review(self, id):
        current_user = request.environ.get('repoze.who.identity')['user']
        ###
        # this is super-hacky, but there was a bug that was causing
        # the current_user object to be None for reasons I cannot
        # ascertain. refreshing the page inexplicably works; hence we
        # do it here. need to test this further.
        ####
        if current_user is None:
            redirect(url(controller="review", action="join_review", id=id))
        else:
            success = self._join_review(id)
            print "\n\n\nOK, review joined.\n%s" % success
            redirect(url(controller="account", action="welcome"))  
        
    
    @ActionProtector(not_anonymous())
    def leave_review(self, id):
        current_user = request.environ.get('repoze.who.identity')['user']
        # for now just adding right away; may want to 
        # ask project lead for permission though.
        reviewer_review_q = model.meta.Session.query(model.ReviewerProject)
        reviewer_reviews = reviewer_review_q.filter(and_(\
                 model.ReviewerProject.review_id == id, 
                 model.ReviewerProject.reviewer_id==current_user.id)).all()
                 
        for reviewer_review in reviewer_reviews:  
            # note that there should only be one entry;
            # this is just in case.   
            model.Session.delete(reviewer_review)
    
        # next, we need to delete all assignments for this person and review
        assignments_q = model.meta.Session.query(model.Assignment)
        assignments = assignments_q.filter(and_(\
                    model.Assignment.review_id == id,
                    model.Assignment.reviewer_id == current_user.id
        )).all()
        
        for assignment in assignments:
            model.Session.delete(assignment)
            
        model.Session.commit()
        redirect(url(controller="account", action="welcome"))
        
        
    @ActionProtector(not_anonymous())
    def export_labels(self, id):
        review_q = model.meta.Session.query(model.Review)
        review = review_q.filter(model.Review.review_id == id).one()
        labels = [",".join(["(internal) id", "pubmed id", "refman id", "labeler", "label"])]
        for citation, label in model.meta.Session.query(\
            model.Citation, model.Label).filter(model.Citation.citation_id==model.Label.study_id).\
            filter(model.Label.review_id==id).all():   
                user_name = self._get_username_from_id(label.reviewer_id)
                labels.append(",".join(\
                   [str(x) for x in [citation.citation_id, citation.pmid_id, citation.refman_id, user_name, label.label]]))
        
        response.headers['Content-type'] = 'text/csv'
        response.headers['Content-disposition'] = 'attachment; filename=labels_%s.csv' % id
        return "\n".join(labels)
        

    @ActionProtector(not_anonymous())
    def delete_review(self, id):
        review_q = model.meta.Session.query(model.Review)
        review = review_q.filter(model.Review.review_id == id).one()

        # make sure we're actually the project lead
        current_user = request.environ.get('repoze.who.identity')['user']
        if not review.project_lead_id == current_user.id:
            return "<font color='red'>tsk, tsk. you're not the project lead, %s.</font>" % current_user.fullname    
    
        ###
        # should probably re-factor in methods...
        ###
        # first delete all associated citations
        citation_q = model.meta.Session.query(model.Citation)
        citations_for_review = citation_q.filter(model.Citation.review_id == review.review_id).all()        
        for citation in citations_for_review:
            model.Session.delete(citation)
        
        # then delete the associations in the table mapping reviewers to 
        # reviews
        reviewer_review_q = model.meta.Session.query(model.ReviewerProject)
        entries_for_review = reviewer_review_q.filter(model.ReviewerProject.review_id == review.review_id).all()
        for reviewer_review in entries_for_review:
            model.Session.delete(reviewer_review)
        
        # next delete all assignments associated with this review
        assignments_q = model.meta.Session.query(model.Assignment)
        assignments = assignments_q.filter(model.Assignment.review_id == review.review_id).all()
        for assignment in assignments:
            model.Session.delete(assignment)
        
        label_q = model.meta.Session.query(model.Label)
        labels = label_q.filter(model.Label.review_id == review.review_id).all()
        for l in labels:
            model.Session.delete(l)
        
        label_feature_q = model.meta.Session.query(model.LabeledFeature)
        labeled_features = label_feature_q.filter(model.LabeledFeature.review_id == review.review_id).all()
        for l in labeled_features:
            model.Session.delete(l)
        
        priority_q = model.meta.Session.query(model.Priority)
        priorities = priority_q.filter(model.Priority.review_id == review.review_id).all()
        for p in priorities:
            model.Session.delete(p)
            
        init_q = model.meta.Session.query(model.InitialAssignment)
        inits = init_q.filter(model.InitialAssignment.review_id == review.review_id).all()
        for init in inits:
            model.Session.delete(init)
        
            
        # finally, delete the review
        model.Session.delete(review)

        model.Session.commit()
        redirect(url(controller="account", action="welcome"))
        
    @ActionProtector(not_anonymous())
    def admin(self, id):
        review_q = model.meta.Session.query(model.Review)
        review = review_q.filter(model.Review.review_id == id).one()
        c.review = review
        c.participating_reviewers = self._get_participants_for_review(id)
        
        # make sure we're actually the project lead
        current_user = request.environ.get('repoze.who.identity')['user']
        if not review.project_lead_id == current_user.id:
            return "<font color='red'>tsk, tsk. you're not the project lead, %s.</font>" % current_user.fullname

        # for the client side
        reviewer_ids_to_names_d = {}
        for reviewer in c.participating_reviewers:
            reviewer_ids_to_names_d[reviewer.id] = reviewer.username
        c.reviewer_ids_to_names_d = reviewer_ids_to_names_d
        
        assignments_q = model.meta.Session.query(model.Assignment)
        assignments = assignments_q.filter(model.Assignment.review_id == id)
        c.assignments = assignments
        return render("/reviews/admin.mako")
            
    @ActionProtector(not_anonymous())
    def show_review(self, id):
        review_q = model.meta.Session.query(model.Review)

        c.review = review_q.filter(model.Review.review_id == id).one()
        # grab all of the citations associated with this review
        citation_q = model.meta.Session.query(model.Citation)
        citations_for_review = citation_q.filter(model.Citation.review_id == id).all()
   
        c.num_citations = len(citations_for_review)
        # and the labels provided thus far
        label_q = model.meta.Session.query(model.Label)
        ### TODO first of all, will want to differentiate between
        # unique and total (i.e., double screened citations). will
        # also likely want to pull additional information here, e.g.,
        # the participating reviewers, etc.
        labels_for_review = label_q.filter(model.Label.review_id == id).all()
        c.num_unique_labels = len(set([lbl.study_id for lbl in labels_for_review]))
        c.num_labels = len(labels_for_review)
        
        # generate a pretty plot via google charts
        chart = PieChart3D(500, 200)
        chart.add_data([c.num_citations-c.num_unique_labels, c.num_unique_labels])
        chart.set_colours(['224499', '80C65A'])
        chart.set_pie_labels(['unscreened', 'screened'])
        c.pi_url = chart.get_url()
        
        reviewer_proj_q = model.meta.Session.query(model.ReviewerProject)
        reviewer_ids = [rp.reviewer_id for rp in reviewer_proj_q.filter(model.Citation.review_id == id).all()]

        c.participating_reviewers = reviewers = self._get_participants_for_review(id)
        user_q = model.meta.Session.query(model.User)
        c.project_lead = user_q.filter(model.User.id == c.review.project_lead_id).one()
        
        current_user = request.environ.get('repoze.who.identity')['user']
        c.is_admin = c.project_lead.id == current_user.id
        n_lbl_d = {} # map users to the number of labels they've provided
        for reviewer in reviewers:
            # @TODO problematic if two reviewers have the same fullname, which
            # isn't explicitly prohibited
            n_lbl_d[reviewer.fullname] = len([l for l in labels_for_review if l.reviewer_id == reviewer.id])
        
        # now make a horizontal bar graph showing the amount of work done by reviewers
        workloads = n_lbl_d.items() # first sort by the number of citations screened, descending
        workloads.sort(key = itemgetter(1), reverse=True)
        num_screened = [x[1] for x in workloads]
        names = [x[0] for x in workloads]
        
        
        ### 
        # so, due to what is apparently a bug in the pygooglechart api, 
        # we construct a google charts string explicitly for the horizontal bar graph here.
        height = 30*len(names)+50
        width = 500
        google_url = "http://chart.apis.google.com/chart?cht=bhg&chs=%sx%s" % (width, height)
        chart = StackedHorizontalBarChart(500, 30*len(names)+50, x_range=(0, c.num_labels))
        data_str = "chd=t:%s" % ",".join([str(n) for n in num_screened])
        google_url = "&".join([google_url, data_str])
        max_num_screened = max(num_screened)
        google_url = "&".join([google_url, "chds=0,%s" % max_num_screened])
        # we have to reverse the names here; this seems to be a quirk with
        # google maps. see: http://psychopyko.com/tutorial/how-to-use-google-charts/
        names.reverse()
        google_url = "&".join([google_url, "chxt=y,x&chxl=0:|%s|" % "|".join([name.replace(" ", "%20") for name in names])])
        # now the x axis labels
        x_ticks = [0, int(max_num_screened/3.0), int(max_num_screened/2.0), int(3 * (max_num_screened/4.0)), max_num_screened]
        google_url = "".join([google_url, "1:|%s" % "|".join([str(x) for x in x_ticks])])
        bar_width = 25
        google_url = google_url + "&chbh=%s&chco=4D89F9" % bar_width
        c.workload_graph_url = google_url

        return render("/reviews/show_review.mako")

    @ActionProtector(not_anonymous())
    def relabel_term(self, term_id, new_label):
        term_q = model.meta.Session.query(model.LabeledFeature)
        labeled_term =  term_q.filter(model.LabeledFeature.id == term_id).one()
        labeled_term.label = new_label
        model.Session.add(labeled_term)
        model.Session.commit()
        redirect(url(controller="review", action="review_terms", id=labeled_term.review_id)) 
        
    @ActionProtector(not_anonymous())
    def delete_term(self, id):
        term_id = id
        term_q = model.meta.Session.query(model.LabeledFeature)
        labeled_term = term_q.filter(model.LabeledFeature.id == term_id).one()
        model.Session.delete(labeled_term)
        model.Session.commit()
        redirect(url(controller="review", action="review_terms", id=labeled_term.review_id)) 
        
        
    @ActionProtector(not_anonymous())
    def label_term(self, review_id, label):
        current_user = request.environ.get('repoze.who.identity')['user']
        new_labeled_feature = model.LabeledFeature()
        new_labeled_feature.term = request.params['term']
        new_labeled_feature.review_id = review_id
        new_labeled_feature.reviewer_id = current_user.id
        new_labeled_feature.label = label
        new_labeled_feature.date_created = datetime.datetime.now()
        model.Session.add(new_labeled_feature)
        model.Session.commit()
        
    
    @ActionProtector(not_anonymous())
    def label_citation(self, review_id, assignment_id, study_id, seconds, label):
        current_user = request.environ.get('repoze.who.identity')['user']
        # check if we've already labeled this; if so, handle
        # appropriately
        label_q = model.meta.Session.query(model.Label)
        existing_label = label_q.filter(and_(
                        model.Label.review_id == review_id, 
                        model.Label.study_id == study_id, 
                        model.Label.reviewer_id == current_user.id)).all()
          
        if len(existing_label) > 0:
            # then this person has already labeled this example
            print "(RE-)labeling citation %s with label %s" % (study_id, label)
            existing_label = existing_label[0]
            existing_label.label = label
            existing_label.label_last_updated = datetime.datetime.now()
            existing_label.labeling_time += int(seconds)
            model.Session.add(existing_label)
            model.Session.commit()
            
            # if we are re-labelng, return the same abstract, reflecting the new
            # label.
            c.cur_lbl = existing_label
            c.assignment_id = c.cur_lbl.assignment_id
            citation_q = model.meta.Session.query(model.Citation)
            c.cur_citation = citation_q.filter(model.Citation.citation_id == study_id).one()
            c.cur_citation = self._mark_up_citation(review_id, c.cur_citation)
            c.review_id = review_id
            return render("/citation_fragment.mako")
        else:
            print "labeling citation %s with label %s" % (study_id, label)
            # first push the label to the database
            new_label = model.Label()
            new_label.label = label
            new_label.review_id = review_id
            new_label.study_id = study_id
            new_label.assignment_id = assignment_id
            new_label.labeling_time = int(seconds)
            new_label.reviewer_id = current_user.id
            new_label.first_labeled = new_label.label_last_updated = datetime.datetime.now()
            model.Session.add(new_label)
            model.Session.commit()
            # pull the associated assignment object
            assignment_q = model.meta.Session.query(model.Assignment)
            assignment = assignment_q.filter(model.Assignment.id == assignment_id).one()
            assignment.done_so_far += 1
            if assignment.assignment_type != "perpetual" and assignment.done_so_far >= assignment.num_assigned:
                assignment.done = True
            model.Session.commit()
            
            # update the number of times this citation has been labeled; 
            # if we have collected a sufficient number of labels, pop it from
            # the queue
            priority_obj = self._get_priority_for_citation_review(study_id, review_id)
            priority_obj.num_times_labeled += 1
            priority_obj.is_out = False
            model.Session.commit()
            
            # are we through with this citation/review?
            review = self._get_review_from_id(review_id)
    
            if review.screening_mode == "single" or \
                    review.screening_mode == "double" and priority_obj.num_times_labeled >= 2:
                model.Session.delete(priority_obj)
                model.Session.commit()
            
            return self.screen_next(review_id, assignment_id)
        
    @ActionProtector(not_anonymous())
    def markup_citation(self, id, assignment_id, citation_id):
        citation_q = model.meta.Session.query(model.Citation)
        c.cur_citation = citation_q.filter(model.Citation.citation_id == citation_id).one()
        c.review_id = id
        c.assignment_id = assignment_id
        c.cur_citation = self._mark_up_citation(id, c.cur_citation)
        
        current_user = request.environ.get('repoze.who.identity')['user']
        label_q = model.meta.Session.query(model.Label)
        c.cur_lbl = label_q.filter(and_(
                                     model.Label.study_id == citation_id,
                                     model.Label.reviewer_id == current_user.id)).all()
        if len(c.cur_lbl) > 0:
            c.cur_lbl = c.cur_lbl[0]
        else:
            c.cur_lbl = None
        return render("/citation_fragment.mako")
      
    @ActionProtector(not_anonymous())
    def screen(self, review_id, assignment_id):
        assignment = self._get_assignment_from_id(assignment_id)
        if assignment is None:
            pdb.set_trace()
            redirect(url(controller="review", action="screen", \
                        review_id=review_id, assignment_id = assignment_id))    
            
            
        review = self._get_review_from_id(review_id)
        if assignment.done:
            redirect(url(controller="account", action="welcome"))    
           
        c.review_id = review_id
        c.review_name = review.name
        c.assignment_id = assignment_id

        c.cur_citation = self._get_next_citation(assignment, review)
        if c.cur_citation is None:
            return render("/assignment_complete.mako")
        c.cur_citation = self._mark_up_citation(review_id, c.cur_citation)
        c.cur_lbl = None
        return render("/screen.mako")
          

    @ActionProtector(not_anonymous())
    def screen_next(self, review_id, assignment_id):
        assignment = self._get_assignment_from_id(assignment_id)
        review = self._get_review_from_id(review_id)

        c.review_id = review_id
        c.review_name = self._get_review_from_id(review_id).name
        c.assignment_id = assignment_id
        
        c.cur_citation = self._get_next_citation(assignment, review)
        
        # but wait -- are we finished?
        if assignment.done or c.cur_citation is None:
            return render("/assignment_complete.mako")
            
        # mark up the labeled terms 
        c.cur_citation = self._mark_up_citation(review_id, c.cur_citation)
        c.cur_lbl = None
        return render("/citation_fragment.mako")
        
        
    def _get_next_citation(self, assignment, review):
        next_id = None
        # if the current assignment is an initial round,
        # we pull from the InitialAssignment table
        if assignment.assignment_type == "initial":
            # in the case of initial assignments, we never remove the citations,
            # thus we need to ascertain that we haven't already screened it
            eligible_pool = self._get_init_ids_for_review(review.review_id)
            # a bit worried about runtime here (O(|eligible_pool| x |already_labeled|))
            # hopefully eligible_pool shrinks as sufficient labels are acquired (and it 
            # shoudl always be pretty small for initial assignments).
            already_labeled = self._get_already_labeled_ids(review.review_id)
            eligible_pool = [xid for xid in eligible_pool if not xid in already_labeled]
            next_id = None
            if len(eligible_pool) > 0:
                next_id = eligible_pool[0]
        else:
            priority = self._get_next_priority(review.review_id)
            if priority is None:
                next_id = None
            else:
                next_id = priority.citation_id
                ## 'check out' / lock the citation
                priority.is_out = True
                priority.locked_by = request.environ.get('repoze.who.identity')['user'].id
                priority.time_requested = datetime.datetime.now()
                model.Session.commit()

        return None if next_id is None else self._get_citation_from_id(next_id)
        
    @ActionProtector(not_anonymous())
    def review_terms(self, id, assignment_id=None):
        review_id = id
        current_user = request.environ.get('repoze.who.identity')['user']
        
        term_q = model.meta.Session.query(model.LabeledFeature)
        labeled_terms =  term_q.filter(and_(\
                                model.LabeledFeature.review_id == review_id,\
                                model.LabeledFeature.reviewer_id == current_user.id
                         )).all()
        c.terms = labeled_terms
        c.review_id = review_id
        c.review_name = self._get_review_from_id(review_id).name
    
        # if an assignment id is given, it allows us to provide a 'get back to work'
        # link.
        c.assignment = assignment_id
        if assignment_id is not None:
            c.assignment = self._get_assignment_from_id(assignment_id)
            
        return render("/reviews/edit_terms.mako")
                         
    @ActionProtector(not_anonymous())
    def review_labels(self, review_id, assignment_id=None):
        current_user = request.environ.get('repoze.who.identity')['user']
        
        label_q = model.meta.Session.query(model.Label)
        already_labeled_by_me = [label for label in label_q.filter(\
                                   and_(model.Label.review_id == review_id,\
                                        model.Label.reviewer_id == current_user.id)).\
                                            order_by(desc(model.Label.label_last_updated)).all()] 
        
        c.given_labels = already_labeled_by_me
        c.review_id = review_id 
        c.review_name = self._get_review_from_id(review_id).name
        
        # now get the citation objects associated with the given labels
        c.citations_d = {}
        for label in c.given_labels:
            c.citations_d[label.study_id] = self._get_citation_from_id(label.study_id)
        
        # if an assignment id is given, it allows us to provide a 'get back to work'
        # link.
        c.assignment = assignment_id
        if assignment_id is not None:
            c.assignment = self._get_assignment_from_id(assignment_id)
     
        return render("/reviews/review_labels.mako")
            
    @ActionProtector(not_anonymous())
    def show_labeled_citation(self, review_id, citation_id):
        current_user = request.environ.get('repoze.who.identity')['user']
        c.review_id = review_id
        c.review_name = self._get_review_from_id(review_id).name
 
        citation_q = model.meta.Session.query(model.Citation)
        c.cur_citation = citation_q.filter(model.Citation.citation_id == citation_id).one()
        # mark up the labeled terms 
        c.cur_citation = self._mark_up_citation(review_id, c.cur_citation)
        
        label_q = model.meta.Session.query(model.Label)
        c.cur_lbl = label_q.filter(and_(
                                     model.Label.study_id == citation_id,
                                     model.Label.reviewer_id == current_user.id)).one()
        c.assignment_id = c.cur_lbl.assignment_id
        return render("/screen.mako")
        
    @ActionProtector(not_anonymous())
    def create_assignment(self, id):
        assign_to = request.params.getall("assign_to")
        due_date = None
        try:
            m,d,y = [int(x) for x in request.params['due_date'].split("/")]
            due_date = datetime.date(y,m,d)
        except:
            pass
        p_rescreen = float(request.params['p_rescreen'])
        n = int(request.params['n'])
        assign_to_ids = [self._get_id_from_username(username) for username in assign_to]
        for reviewer_id in assign_to_ids:     
            new_assignment = model.Assignment()
            new_assignment.review_id = id
            new_assignment.reviewer_id = reviewer_id
            new_assignment.date_due = due_date
            new_assignment.done = False
            new_assignment.done_so_far = 0
            new_assignment.num_assigned = n
            new_assignment.p_rescreen = p_rescreen
            new_assignment.date_assigned = datetime.datetime.now()
            model.Session.add(new_assignment)
            model.Session.commit()
        
        redirect(url(controller="review", action="join_review", id=id))     
              
        
    def _get_priority_for_citation_review(self, citation_id, review_id):
        priority_q = model.meta.Session.query(model.Priority)
        p_for_cit_review =  priority_q.filter(and_(\
                                model.Priority.review_id == review_id,\
                                model.Priority.citation_id == citation_id,\
                         )).one()
        return p_for_cit_review
        
    def _join_review(self, review_id):
        current_user = request.environ.get('repoze.who.identity')['user']
        
        # first, make sure this person isn't already in this review.
        reviewer_review_q = model.meta.Session.query(model.ReviewerProject)
        reviewer_reviews = reviewer_review_q.filter(and_(\
                 model.ReviewerProject.review_id == review_id, 
                 model.ReviewerProject.reviewer_id == current_user.id)).all()
        
        if len(reviewer_reviews) == 0:
            # we only add them if they aren't already a part of the review.
            reviewer_project = model.ReviewerProject()
            reviewer_project.reviewer_id = current_user.id
            reviewer_project.review_id = review_id
            model.Session.add(reviewer_project)
        
            # now we check what type
            review = self._get_review_from_id(review_id)
            if review.screening_mode in (u"single", u"double"):
                # then we automatically add a `perpetual' assignment
                self._make_perpetual_assignment(current_user.id, review_id)
                
            if review.initial_round_size > 0:
                self._make_initial_assignment(current_user.id, review_id)

            model.Session.commit()
            return True
        return False     
            
    def _get_next_priority(self, review_id):
        '''
        returns citation ids to be screened for the specified
        review, ordered by their priority (int he priority table).
        this is effectively how AL is implemented in our case --
        we assume the table has been sorted/ordered by some
        other process.
        
        Note: this will not return ids for instances that are 
        currently being labeled.
        '''
        priority_q = model.meta.Session.query(model.Priority)
        me = request.environ.get('repoze.who.identity')['user'].id
        ranked_priorities = [priority for priority in priority_q.filter(\
                                model.Priority.review_id == review_id).\
                                    order_by(model.Priority.priority).all() if\
                                    not (priority.is_out and priority.locked_by != me)]
                                    
        best_that_i_havent_labeled = None
        already_labeled = self._get_already_labeled_ids(review_id)
        for priority_obj in ranked_priorities:
             if priority_obj.citation_id not in already_labeled:
                 return priority_obj
        # this person has already labeled everything -- nothing more to do!
        return None
        
    def _get_init_ids_for_review(self, review_id):
        init_q = model.meta.Session.query(model.InitialAssignment)
        init_ids = [ia.citation_id for ia in \
                     init_q.filter(model.InitialAssignment.review_id == review_id).\
                        order_by(model.InitialAssignment.citation_id).all()]    
        return init_ids
    
    def _get_already_labeled_ids(self, review_id):
        ''' 
        returns a list of citation ids corresponding to those citations that
        the current reviewer has labeled for the specified review.
        '''
        reviewer_id = request.environ.get('repoze.who.identity')['user'].id
        label_q = model.meta.Session.query(model.Label)
        already_labeled_ids = [label.study_id for label in label_q.filter(and_(\
                                                    model.Label.review_id == review_id,\
                                                    model.Label.reviewer_id == reviewer_id)).all()]
        return already_labeled_ids 
        
    def _get_participants_for_review(self, review_id):
        reviewer_proj_q = model.meta.Session.query(model.ReviewerProject)
        reviewer_ids = \
            list(set([rp.reviewer_id for rp in reviewer_proj_q.filter(model.ReviewerProject.review_id == review_id).all()]))
        user_q = model.meta.Session.query(model.User)
        reviewers = [user_q.filter(model.User.id == reviewer_id).one() for reviewer_id in reviewer_ids]
        return reviewers
    
    def _get_username_from_id(self, id):
        user_q = model.meta.Session.query(model.User)
        return user_q.filter(model.User.id == id).one().username    
        
    def _get_id_from_username(self, username):
        user_q = model.meta.Session.query(model.User)
        return user_q.filter(model.User.username == username).one().id
        
    def _get_review_from_id(self, review_id):
        review_q = model.meta.Session.query(model.Review)
        return review_q.filter(model.Review.review_id == review_id).one()
        
    def _get_citations_for_review(self, review_id):
        citation_q = model.meta.Session.query(model.Citation)
        citations_for_review = citation_q.filter(model.Citation.review_id == review_id).all()
        return citations_for_review
        
    def _get_citation_from_id(self, citation_id):
        citation_q = model.meta.Session.query(model.Citation)
        return citation_q.filter(model.Citation.citation_id == citation_id).one()
        
    def _get_assignment_from_id(self, assignment_id):
        assignment_q = model.meta.Session.query(model.Assignment)
        try:
            return assignment_q.filter(model.Assignment.id == assignment_id).one()
        except:
            return None
        
    def _make_perpetual_assignment(self, reviewer_id, review_id):
        new_assignment = model.Assignment()
        new_assignment.review_id = review_id
        new_assignment.reviewer_id = reviewer_id
        new_assignment.date_due = None # TODO
        new_assignment.done = False
        new_assignment.done_so_far = 0
        new_assignment.num_assigned = -1 # this is meaningless for `perpetual' assignments
        new_assignment.date_assigned = datetime.datetime.now()
        new_assignment.assignment_type = u"perpetual"
        model.Session.add(new_assignment)
        model.Session.commit()
    
    def _make_initial_assignment(self, reviewer_id, review_id):
        new_assignment = model.Assignment()
        new_assignment.review_id = review_id
        new_assignment.reviewer_id = reviewer_id
        new_assignment.date_due = None # TODO
        new_assignment.done = False
        new_assignment.done_so_far = 0
        new_assignment.num_assigned = self._get_review_from_id(review_id).initial_round_size
        new_assignment.date_assigned = datetime.datetime.now()
        new_assignment.assignment_type = u"initial"
        model.Session.add(new_assignment)
        model.Session.commit()
        
    def _create_initial_assignment_for_review(self, review_id, n):
        # picks a random set of the citations from the
        # specified review and adds them into the
        # FixedAssignment table -- participants
        # in this review should subsequently be tasked
        # with Assignments that reference this 
        
        # first grab some ids at random
        init_ids = random.sample([citation.citation_id for citation in self._get_citations_for_review(review_id)], n)
        for citation_id in init_ids:
            init_a = model.InitialAssignment()
            init_a.review_id = review_id
            init_a.citation_id = citation_id
            model.Session.add(init_a)
            model.Session.commit()
            
    def _mark_up_citation(self, review_id, citation):
        # pull the labeled terms for this review
        labeled_term_q = model.meta.Session.query(model.LabeledFeature)
        reviewer_id = request.environ.get('repoze.who.identity')['user'].id
        labeled_terms = labeled_term_q.filter(and_(\
                            model.LabeledFeature.review_id == review_id,\
                            model.LabeledFeature.reviewer_id == reviewer_id)).all()
        citation.marked_up_title = citation.title
        citation.marked_up_abstract = citation.abstract
        for term in labeled_terms:
            title_matches = list(set(re.findall(term.term, citation.marked_up_title)))

            for match in title_matches:
                citation.marked_up_title = citation.marked_up_title.replace(match, "<font color='%s'>%s</font>" % (COLOR_D[term.label], match))
            
            if citation.marked_up_abstract is not None:
                abstract_matches = list(set(re.findall(term.term, citation.marked_up_abstract)))
                for match in abstract_matches:
                    citation.marked_up_abstract = \
                       citation.marked_up_abstract.replace(match, "<font color='%s'>%s</font>" % (COLOR_D[term.label], match))
            else:
                citation.marked_up_abstract = ""
        citation.marked_up_title = literal(citation.marked_up_title)
        citation.marked_up_abstract = literal(citation.marked_up_abstract)
        return citation
   
        


