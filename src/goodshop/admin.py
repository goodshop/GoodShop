from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Category, User

class ImageInline(admin.StackedInline):
    model = ProductImage
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    list_editable = ('name',)

    def image(self, product):
        url = [image.get_img_url() for image in ProductImage.objects.filter(product=product)]
        tag = []
        for u in url[0:4]:
            tag.append(
                "<div width='180px' height='180px' style='float: left;'>"
                "<img src='%s' style='max-width: 180px; max-height: 180px;'>"
                "</div>" % u
                )
        return "".join(tag)

    image.allow_tags = True
    inlines = [ImageInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)