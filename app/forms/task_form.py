#! /usr/bin/env python

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class AddTask(Form):
	task_name = StringField(u'Task Title', validators = [Required()])
    task_desc  = StringField(u'Task Description', validators = [Required()]

    task_category = StringField(u'Task Category', validators = [Required()])
    task_urgency = BooleanField(u'Task is Urgent', validators = [Required()])
    due_date = StringField(u'Due Date', validators = [Required()])