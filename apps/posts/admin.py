from django.contrib import admin

from .models import Post, Media, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'date_created')
    search_fields = ('author__username',)
    list_filter = ('author', 'date_created')
    readonly_fields = ('date_created',)
    save_on_top = True
    save_as = True


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('media_type', 'post')
    search_fields = ('post__id',)
    list_filter = ('media_type', 'post')
    save_on_top = True
    save_as = True


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'author')
    search_fields = ('post__id', 'author__username')
    list_filter = ('post', 'author')
    save_on_top = True
    save_as = True


admin.site.site_title = 'Social Network'
admin.site.site_header = 'Social Network'
