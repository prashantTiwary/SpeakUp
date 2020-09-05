from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, Textarea



class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    
    def liked(self, post_id):
        if Likes.objects.get(user=self.id, post=post_id):
            return True
        else:
            return False

    

class Post(models.Model):
    text = models.CharField(max_length=280,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def get_likes(self):
        return Likes.objects.filter(post=self.id).count()


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')


class textForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {
            'text': 'Create New Post  '
        }
        widgets = {
            'text': Textarea(attrs={'class': 'post-field', 'placeholder': 'Type Something...'})
        }
