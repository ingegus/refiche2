from django import template
from django.contrib.auth.forms import PasswordChangeForm
from app.functions import getStudent
from registration.forms import ChangeUserInfosForm


register = template.Library()

@register.inclusion_tag('registration/change_user_infos.html')
def getStudentAccountForm(request):
	""" Get the managing account form and adds the context """

	student = getStudent(request.user)

	form = ChangeUserInfosForm(
			initial={ 'firstName': student.user.first_name,
					  'lastName': student.user.last_name }
		)

	return locals()