# coding=UTF-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save, pre_delete
from app.functions import renameFile, addFile, deleteFile, deleteUser, getLastSheetsForLesson


class Lesson(models.Model):
	""" The lesson/class model, they can only be created by a delegate """

	name = models.CharField(max_length=30)  # The official name of the class
	teacher = models.ForeignKey('Teacher')  # The link to the teacher (one teacher for one class)

	def __str__(self):
		return "{0} ({1})".format(self.name, self.teacher)

	def getLastSheets(self):
		""" Return the 2 last sheets for the lesson """
		return getLastSheetsForLesson(self, 2)


class Level(models.Model):
	""" Level/ degree model, they can only be created by myself now
        It might change in the future"""

	name = models.CharField(max_length=30)  # The official name of the level/degree

	def __str__(self):
		return self.name


class School(models.Model):
	""" School model, it can refer to many levels (primaire, collège ...) """

	name = models.CharField(max_length=255)  # The full name of the school chosen by the user
	levels = models.ManyToManyField(Level)  # Link with the levels of the school

	def __str__(self):
		return self.name


class Classroom(models.Model):
	""" Classroom model, it always refer to at least on profile """

	level = models.ForeignKey('Level')  # Level or degree of the class (ex: 1ere)
	school = models.ForeignKey('School')  # School witch the classroom belongs to
	name = models.CharField(max_length=100)  # Name of the classroom (ex: Première S-3)
	shortName = models.CharField(max_length=8)  # Name of the classroom shortened (ex: 1-S3)
	lessons = models.ManyToManyField(Lesson)

	def __str__(self):
		return self.name


class Profile(models.Model):
	""" Abstract User profile, it extends the original User class
        and is made to become weather a student or a teacher etc.. """

	user = models.OneToOneField(User)  # Link with the original user class that we extend
	classroom = models.ForeignKey('Classroom')  # Link to the user's classroom
	school = models.ForeignKey('School')  # Link to the school of the profile (student or teacher)
	# I will add some other things but now this is it

	class Meta(object):
		abstract = True


class Student(Profile):
	""" Student model, it extends the abstract Profile and the User
        model """

	lessons = models.ManyToManyField(Lesson)
	numberOfSheetsUploaded = models.IntegerField(default=0)

	def __str__(self):
		return "Profil de {0}".format(self.user.username)


class Teacher(models.Model):
	""" Teacher model, it does not extends the profile abstract but
        might do in the future if some want to connect to refiche """

	GENDER_CHOICES = (('M.', 'Monsieur'),
					  ('Mme', 'Madame'),
					  ('Mlle', 'Mademoiselle'))

	lastName = models.CharField(max_length=60)  # Last name of the teacher
	firstName = models.CharField(max_length=30, null=True)  # First name of the teacher
	gender = models.CharField(max_length=4, choices=GENDER_CHOICES)
	createdBy = models.ForeignKey(Student)

	def __str__(self):
		return "{0} {1}".format(self.gender, self.lastName)


class Chapter(models.Model):
	""" Chapter model  """

	name = models.CharField(max_length=255)
	number = models.IntegerField()
	lesson = models.ForeignKey('Lesson')

	def __str__(self):
		return '{}. {}'.format(self.number, self.name)


class Sheet(models.Model):
	""" Sheet model (card, notes about a lesson etc) """

	SHEET_TYPE_CHOICES = (('SHEET', 'fiche'),
						  ('NOTES', 'cours'),
						  ('TEST', 'sujetDeContrôle'),
						  ('TEST_CORRECTION', 'corrigéDeContrôle'))

	name = models.CharField(max_length=100)
	extension = models.CharField(max_length=50)
	chapter = models.ForeignKey('Chapter', null=True, verbose_name="chapitre")
	lesson = models.ForeignKey('Lesson', verbose_name="matière")
	sheetType = models.CharField(max_length=50, choices=SHEET_TYPE_CHOICES, default='SHEET', verbose_name="catégorie")

	sheetFile = models.FileField(upload_to=renameFile, verbose_name="fichier")
	uploadedBy = models.ForeignKey(Student)
	contentType = models.CharField(max_length=255)
	uploadDate = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return '{}{}'.format(self.name, self.extension)


# _____________________________________________________________________
# SIGNALS

post_save.connect(addFile, sender=Sheet)
post_delete.connect(deleteFile, sender=Sheet)
pre_delete.connect(deleteUser, sender=User)