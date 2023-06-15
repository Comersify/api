from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Friends(models.Model):
    user    = models.OneToOneRel(User, on_delete=models.CASCADE)
    friends = models.ManyToManyRel(User)

    def __str__(self) -> str:
        return f"Friends of: {self.user}" 
    

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=True)

