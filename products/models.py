from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        

class Product(models.Model):
    LABEL_CHOICES = [
        ('giveaway', 'Giveaway'),
        ('exchange', 'Exchange'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default=" ")
    location = models.URLField()
    label = models.CharField(
        max_length=10,
        choices=LABEL_CHOICES,
        default='giveaway'
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()
        
        if not self.name:
            raise ValidationError({'name': 'Product name cannot be empty'})
            
        if self.description and len(self.description.strip()) == 0:
            raise ValidationError({'description': 'Description cannot be empty if provided'})
            
        if self.label not in dict(self.LABEL_CHOICES):
            raise ValidationError({'label': f'Invalid label choice. Must be one of: {", ".join(dict(self.LABEL_CHOICES).keys())}'})
            
        try:
            URLValidator()(self.location)
        except ValidationError:
            raise ValidationError({'location': 'Please enter a valid URL'})
        

class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.product and self.product.pictures.count() >=5:
            raise ValidationError("A product can have a maximum of 5 pictures.")

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies'
    )
    text = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:30] if self.text else "Comment with picture"

    def like_count(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Tracks the user who liked the comment
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')  # Ensures a user can like a comment only once
