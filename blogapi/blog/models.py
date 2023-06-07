from blogapi.common.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class Article(BaseModel):
    """Model definition for Article."""
    PUBLISHED = 'p'
    REVIWING = 'r'
    FAILED = 'f'
    DRAFT = 'd'
    status_choices = (
        (PUBLISHED, _('published')),
        (REVIWING, _('reviwing')),
        (FAILED, _('rejected')),
        (DRAFT, _('draft')),
    )


    title = models.CharField(_("title"), max_length=50, blank=False, null=False)
    description = models.TextField(_("description"), blank=False, null=False)
    slug = models.SlugField(_("slug"), blank=False, null=False)
    author = models.ForeignKey(User,verbose_name=_('author'),on_delete=models.DO_NOTHING,related_name='articles')
    category = models.ManyToManyField('Category',verbose_name=_('category'),related_name='articles')
    type = models.ForeignKey('ArticleType',verbose_name=_('type'),on_delete=models.SET_NULL,blank=True,null=True)
    status = models.CharField(_('status'), max_length=1, choices=status_choices, default=REVIWING)
    image = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='articles')
    class Meta:
        """Meta definition for Article."""

        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        """Unicode representation of Article."""
        return f'{self.title} by : {self.author}'

    def save(self):
        """Save method for Article."""
        pass

    def get_absolute_url(self):
        """Return absolute url for Article."""
        from django.urls import reverse
        return reverse("article-detail", kwargs={"slug": self.slug})



class Category(BaseModel):
    """ Model definition for Category."""

    title = models.CharField(_('title'),blank=False,null=False, max_length=50)
    slug = models.SlugField(_('slug'),unique=True,null=True)
    position = models.IntegerField(_('position'), default=1)
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=_("parent"), on_delete=models.SET_NULL,
                               related_name='childs')

    class Meta:
        """Meta definition for Category."""

        verbose_name='Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Unicode representation of Article."""
        return f'{self.title}'
    
    def get_absolute_url(self):
        """Return absolute url for Article."""
        from django.urls import reverse
        return reverse("category-detail", kwargs={"slug": self.slug})
    
class ArticleType(BaseModel):
    """Model definition for Article Type."""

    name = models.CharField(_('name'), max_length=50)
    class Meta:
        """Meta definition for Article Type."""

        verbose_name = 'Article Type'
        verbose_name_plural = 'Articles Type'

    def __str__(self):
        """Unicode representation of Article Type."""
        return self.name
    

class Image(BaseModel):
    """Model definition for Image."""
    alt = models.CharField(_('image alt'),null=True, blank=True, max_length=100)
    img= models.ImageField(_('image'),upload_to='images')
    

    class Meta:
        """Meta definition for Image."""

        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        """Unicode representation of Image."""
        return f'{self.alt}'


