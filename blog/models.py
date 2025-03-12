from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.post_set.all().count()}"
    
    class Meta:
        ordering = ("last_name",)


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    
    def __str__(self):
        return self.tag
    
    def post_list(self):
        post_list = [str(post.pk) for post in self.post_set.all()]
        if len(post_list) > 0:
            post_list = ", ".join(post_list)
        else:
            post_list = "no posts"
        return post_list
    
    class Meta:
        ordering = ["tag"]
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=200, default="")
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    slug = models.SlugField(default = "", null = False,
                            blank = True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
    def tag_list(self):
        tag_list = [tag.tag for tag in self.tag.all()]
        tag_list = ", ".join(tag_list)
        return tag_list

    def get_absolute_url(self):
        return reverse("post-detail-page", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        
        # Set up excerpt field
        if len(self.content) > 100: # set exerpt (saved in slug section)
            last_space_index = self.content[:100].rfind(" ")
            self.excerpt = f"{self.content[:last_space_index]}..."
        else:
            self.excerpt = f"{self.content}..."

        # Set up slug field
        #Test if existing or new
        if not self.pk: # New
            super().save(*args, **kwargs)
            self.slug = slugify("-".join((self.title, str(self.pk))))
        else: # Existing
            self.slug = slugify("-".join((self.title, str(self.pk))))

        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-date", "title")

class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
                             related_name="comments")
    
    def __str__(self):
        text = self.text
        post = self.post.title
        if len(text) > 50:
            spc_pos = text[:50].rfind(" ")
            text = text[:spc_pos]
        return f"{text} [{post}]"

    class Meta:
        ordering = ["-pk"]

# # --- Routine to add images to ImageField in db ---#
# from blog.models import Post
# from django.core.files import File

# for i in range(0:101):
#     post, created = Post.objects.get_or_create(id=i)
#     with open(f'./blog/static/blog/images/{i:04d}_pic.jpg', 'rb') as f:
#         django_file = File(f)
#         post.image.save(f'{i:04d}_pic.jpg', django_file)

# p1 = Post.objects.get(id=1)
# print(p1.image)
# posts/0001_pic.jpg

# # to test:

# if p.image:
#     print("Yes")
# else:
#     print("No")