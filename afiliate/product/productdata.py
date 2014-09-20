from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder


from afiliate.product import MessageFactory as _


class IProductData(form.Schema, IImageScaleTraversable):
    """
    Prodcut data for affiliate program.
    """
    programName = schema.TextLine(
        title=_(u"Program name"),
        description=_(u"Nname of the advertiser program associated with the product."),
        required=True,
    )

    programUrl = schema.URI(
        title=_(u"Program url"),
        description=_(u"URL of advertiser's primary page (usually the home page), include http://"),
        required=True,
    )

    catalogName = schema.TextLine(
        title=_(u"Catalog name"),
        description=_(u"Indicates the name of the associated product catalog."),
        required=True,
    )

    lastUpdated = schema.Datetime(
        title=_(u"Last updated"),
        description=_(u"Date of the most recent update to the product."),
        required=True,
    )

    productName = schema.TextLine(
        title=_(u"Product's name"),
        description=_(u"The product's name"),
        required=True,
    )

    keywords = schema.TextLine(
        title=_(u"Keywords"),
        description=_(u"A set of keywords describing the product, which can be separated by commas or spaces."),
        required=True,
    )

    # description, use dexterity content type default description field (Summary).

    sku = schema.TextLine(
        title=_(u"SKU"),
        description=_(u"Advertiser's unique identifier for the product."),
        required=True,
    )

    manufacturer = schema.TextLine(
        title=_(u"Manufacturer"),
        description=_(u"The brand or manufacturer of the product."),
        required=True,
    )

    manufacturerId = schema.TextLine(
        title=_(u"Manufacturer ID"),
        description=_(u"Manufacturer's unique product code."),
        required=True,
    )
#Note!!!:  sku + manufacturerId , can identifier the same product !!!??

    upc = schema.TextLine(
        title=_(u"UPC"),
        description=_(u"12-digit UPC, or 13-digit EAN number."),
        required=False,
    )

    isbn = schema.TextLine(
        title=_(u"ISBN"),
        description=_(u"ISBN number, if available. This is a unique, machine-readable identification number that is often applied to books."),
        required=False,
    )
#note!!!: ISBN can identifier the same product !!!??

    currency = schema.TextLine(
        title=_(u"Currency"),
        description=_(u"The three-letter currency code that specifies the currency for the product prices, default value is 'USD'"),
        default=_(u"USD"),
        required=True,
    )





class ProductData(Container):
    grok.implements(IProductData)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IProductData)
    grok.require('zope2.View')
    grok.name('view')
