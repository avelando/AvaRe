from django.db import models

class UserProfile(models.Model):
    name = models.CharField("Nome do usuário", max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (ID {self.pk})"


class FeedbackDataset(models.Model):
    feedback_id = models.CharField(max_length=50)
    id_prompt = models.CharField(max_length=255)
    prompt = models.TextField(blank=True, null=True)
    supporting_text = models.TextField(blank=True, null=True)
    essay_title = models.CharField(max_length=255, blank=True, null=True)
    essay_text = models.TextField()
    essay_year = models.PositiveIntegerField(blank=True, null=True)
    general_comment = models.TextField(blank=True, null=True)
    c1 = models.TextField(blank=True, null=True)
    c2 = models.TextField(blank=True, null=True)
    c3 = models.TextField(blank=True, null=True)
    c4 = models.TextField(blank=True, null=True)
    c5 = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.feedback_id


class LlmsDataset(models.Model):
    topic = models.CharField(max_length=255)
    sup_text = models.TextField(blank=True, null=True)
    essay = models.TextField()
    c1 = models.TextField(blank=True, null=True)
    c2 = models.TextField(blank=True, null=True)
    c3 = models.TextField(blank=True, null=True)
    c4 = models.TextField(blank=True, null=True)
    c5 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.topic} — {self.essay[:30]}…"


class UserResponse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    feedback = models.ForeignKey(FeedbackDataset, on_delete=models.CASCADE)
    llm = models.ForeignKey(LlmsDataset, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    CHOICES = [
        ("human", "Humano"),
        ("ia", "IA"),
    ]
    choice_c1 = models.CharField("Competência 1", max_length=5, choices=CHOICES)
    choice_c2 = models.CharField("Competência 2", max_length=5, choices=CHOICES)
    choice_c3 = models.CharField("Competência 3", max_length=5, choices=CHOICES)
    choice_c4 = models.CharField("Competência 4", max_length=5, choices=CHOICES)
    choice_c5 = models.CharField("Competência 5", max_length=5, choices=CHOICES)

    class Meta:
        verbose_name = "Resposta do usuário"
        verbose_name_plural = "Respostas dos usuários"
        unique_together = ("user", "feedback", "llm")

    def __str__(self):
        return f"{self.user.name} — {self.feedback.feedback_id}"
