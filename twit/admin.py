from django.contrib import admin

from .models import Comment, Tweet

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3

class TweetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['tweet_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [CommentInline]
    list_display = ('tweet_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['tweet_text']


admin.site.register(Tweet, TweetAdmin)
admin.site.register(Comment)
