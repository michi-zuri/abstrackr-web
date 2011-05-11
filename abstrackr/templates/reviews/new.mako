<%inherit file="../site.mako" />
<%def name="title()">new review</%def>

<div class="breadcrumbs">
  ./<a href="${url(controller='account', action='welcome')}">dashboard</a>
</div>

<div class="content">
<center>
<table class="form_table">
 ${h.form(url(controller='review', action='create_review_handler'), multipart=True)}
    <tr><td><label>project name:</td><td> ${h.text('name')}</label></td></tr>
    <tr><td><label>project description:</td> <td>${h.textarea('description', rows="10", cols="40")}</label></td></tr>
    <tr><td><label>upload file (list of PMIDs or refman XML):</td> <td>${h.file('db')} </label></td></tr>
    <tr><td><label>screening mode:</td> <td>${h.select("screen_mode", None, ["Single-screen", "Double-screen", "Advanced"])} </label></td></tr>
    <tr><td><label>order abstracts by:</td> <td>${h.select("order", None, ["Random", "Most likely to be relevant", "Most ambiguous"])} </label></td></tr>
    <tr><td><label>initial round size:</td><td> ${h.text('init_size', '0')}</label></td></tr>
    <tr><td></td><td></td><td>${h.submit('post', 'Create new review')}</td></tr>
  ${h.end_form()} 
</table>

</center>


</div>