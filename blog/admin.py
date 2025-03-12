from django.contrib import admin

# Register your models here.
from .models import Author, Post, Tag, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "author", "tag_list")
    list_filter = ("author", "tag", "date")
    prepopulated_fields = {"slug": ("title",)}

    def save_related(self, request, form, formsets, change):
        # Get the 'tag' ManyToManyField instance from the 'Post' model instance
        tag_field = getattr(form.instance, 'tag')

        # Retrieve existing tags associated with the post
        existing_tags = tag_field.all()

        # Get the selected tags from the form data
        selected_tags = request.POST.getlist('tag')

        # Merge existing tags with newly selected tags and remove duplicates
        updated_tags = list(existing_tags) + list(tag_field.model.objects.filter(pk__in=selected_tags))
        updated_tags = list(set(updated_tags))

        # Update the 'tag' ManyToManyField with new and existing instances
        form.instance.tag.set(updated_tags)

        form.save_m2m()

        # Save the form
        super().save_related(request, form, formsets, change)
        print(f"Sel tags: {selected_tags} ({len(selected_tags)})")
        print(f"Exs tags: {existing_tags} ({len(existing_tags)})")
        print(f"Upd tags: {updated_tags} ({len(updated_tags)})")

class TagAdmin(admin.ModelAdmin):
    list_display = ("tag", "post_list")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")

admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)