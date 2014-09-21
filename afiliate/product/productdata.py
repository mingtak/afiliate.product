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

from plone.indexer import indexer

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

    salePrice = schema.Float(
        title=_(u"Sale price"),
        description=_(u"Optional sale price for the product if different from the actual price."),
        required=False,
    )

    price = schema.Float(
        title=_(u"Price"),
        description=_(u"The selling price of the product (decimal format)."),
        required=False,
    )

    retailPrice = schema.Float(
        title=_(u"Retail price"),
        description=_(u"The retail price or manufacturer suggested retail price of the product."),
        required=False,
    )

    fromPrice = schema.TextLine(
        title=_(u"From price"),
        description=_(u"This is a flag indicating if the price should be displayed with a caveat indicating that the actual price may be different."),
        required=False,
    )

    buyUrl = schema.URI(
        title=_(u"Buy URL, include 'http://'"),
        description=_(u"The URL of the page at which a shopper can buy the product. This is converted into a click tracking URL containing the product Ad ID, publisher Web site ID and BUYURL."),
        required=True,
    )

# required is True or False ?
    impressionUrl = schema.URI(
        title=_(u"Impression URL, include 'http://'"),
        description=_(u"Impression tracking code. This is an image tag for a 1x1 pixel that uses the product's Ad ID and the subscription's Web site ID. This must be displayed in order to track impressions for the product."),
        required=False,
    )

    imageUrl = schema.URI(
        title=_(u"Image URL, include 'http://'"),
        description=_(u"Location of the advertiser-hosted product image."),
        required=False,
    )

    advertiserCategory = schema.TextLine(
        title=_(u"Advertiser category"),
        description=_(u"This field is populated by advertisers who are using their own category scheme for products."),
        required=False,
    )

    thirdPartyId = schema.TextLine(
        title=_(u"Third party ID"),
        description=_(u"Used by an advertiser for a publisher's category ID or any other information used to tailor a catalog to a specific publisher."),
        required=False,
    )

    thirdPartyCategory = schema.TextLine(
        title=_(u"Third party category"),
        description=_(u"Third party category, may be comma-separated. Used to tailor a product catalog to a specific publisher's category structure."),
        required=False,
    )

    author = schema.TextLine(
        title=_(u"Author"),
        description=_(u"Used for books."),
        required=False,
    )

    artist = schema.TextLine(
        title=_(u"Artist"),
        description=_(u"Used for recorded media."),
        required=False,
    )

    publicationTitle = schema.TextLine(
        title=_(u"Publication title"),
        description=_(u"Used for books and recorded media."),
        required=False,
    )

    publisher = schema.TextLine(
        title=_(u"Publisher"),
        description=_(u"Used for books."),
        required=False,
    )

    label = schema.TextLine(
        title=_(u"Label"),
        description=_(u"Publisher of recorded media(Sony, etc)."),
        required=False,
    )

    format = schema.TextLine(
        title=_(u"Format"),
        description=_(u"For example: CD=Compact Disc, MC=Cassette, LP=Long Play Record, DVD=Digital Video Disk, VHS=VHS Video."),
        required=False,
    )

    special = schema.TextLine(
        title=_(u"Special"),
        description=_(u"Used to denote a special offer. Can be used by a publisher to identify unique products, Will be YES, NO or empty."),
        required=False,
    )

    gift = schema.TextLine(
        title=_(u"Gift"),
        description=_(u"Indicates whether or not the product is suggested as a gift item, Will be YES, NO or empty."),
        required=False,
    )

    promotionalText = schema.TextLine(
        title=_(u"Promotional text"),
        description=_(u"Short text accompanying a promotion."),
        required=False,
    )

    #startDate, endDate, useing dexterity behavior

    offLine = schema.TextLine(
        title=_(u"Offline"),
        description=_(u"Indicates whether the offer is available offline (as in available through retail store), Will be YES, NO or empty."),
        required=False,
    )

    onLine = schema.TextLine(
        title=_(u"Online"),
        description=_(u"Indicates whether the offer is available online (as in available through Web site), Will be YES, NO or empty."),
        required=False,
    )

    inStock = schema.TextLine(
        title=_(u"In stock"),
        description=_(u"Indicates whether the product is currently in the advertiser's inventory, Will be YES or NO."),
        required=False,
    )

    condition = schema.TextLine(
        title=_(u"Condition"),
        description=_(u"Condition of product, ex. 'Will be New', 'Used' or 'Refurbished'."),
        required=False,
    )

    warranty = schema.TextLine(
        title=_(u"Warranty"),
        description=_(u"Description of warranty accompanying the product."),
        required=False,
    )

    standardShippingCost =schema.Float(
        title=_(u"Standard shipping cost"),
        description=_(u"Usually is the cost for the typical standard, lowest cost shipping method. This is provided for informational purposes and the actual shipping cost could vary depending on the visitor."),
        required=False,
    )

@indexer(IProductData)
def keywords_indexer(obj):
    keywordsList = obj.keywords.split(',')
    return keywordsList
grok.global_adapter(keywords_indexer, name='keywords')

@indexer(IProductData)
def thirdPartyCategory_indexer(obj):
    thirdPartyCategoryList = obj.thirdPartyCategory.split(',')
    return thirdPartyCategoryList
grok.global_adapter(thirdPartyCategory_indexer, name='thirdPartyCategory')


class ProductData(Container):
    grok.implements(IProductData)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IProductData)
    grok.require('zope2.View')
    grok.name('view')
