from django.db import models

class Area(models.Model):
    name = models.CharField(max_length=255)

class User(models.Model):
    payroll_number = models.PositiveBigIntegerField(primary_key=True, null=False, unique=True)
    password = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.PositiveIntegerField()
    min_gender = models.BooleanField()
    min_general = models.BooleanField()
    role = models.IntegerField()
    status = models.BooleanField()
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)

class Training(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    attendance_code = models.CharField(max_length=5)
    modality = models.BooleanField()
    general = models.BooleanField()
    internal = models.BooleanField()
    status = models.BooleanField()

class Invitation(models.Model):
    description = models.CharField(max_length=255)
    optional = models.BooleanField()
    status = models.BooleanField()
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)

class Date(models.Model):
    day = models.DateField()

class Question(models.Model):
    description = models.CharField(max_length=255)

class User_Invitation(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    invitation_id = models.ForeignKey(Invitation, on_delete=models.CASCADE)

class User_Training(models.Model):
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance = models.BooleanField()
    certified = models.BooleanField()

class Certificate(models.Model):
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    external = models.BooleanField()
    status = models.BooleanField()

class Evaluation(models.Model):
    type = models.IntegerField()
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Date_Training(models.Model):
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    date_id = models.ForeignKey(Date, on_delete=models.CASCADE)
    time = models.TimeField()

class Evaluation_Question(models.Model):
    evaluation_id = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)

class DNC(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=65535)
    status = models.BooleanField()

class Needs_Request(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=65535)
    status = models.BooleanField()
    
    