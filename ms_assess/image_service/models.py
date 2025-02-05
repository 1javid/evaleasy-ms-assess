from django.db import models

class AssessmentResult(models.Model):
    assessment_id = models.CharField(max_length=255)  # Reference to the test’s assessmentID
    student_id = models.CharField(max_length=255)     # Student’s ID
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    variant = models.CharField(max_length=50)
    answers = models.JSONField()       # Student answers as received from the image service
    correct_answers = models.JSONField()  # Correct answers fetched from the test microservice
    answer_sheet = models.BinaryField()     # The image data (binary) for the student’s answer sheet
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.assessment_id} - {self.student_id}"
