from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer
from lxml import etree
from plone.memoize.instance import memoizedproperty
from zope.interface import Interface
from zope.interface import implements
import os


class IMultiLayersView(Interface):
    """ """


class KMLFile(BrowserView):

    """ Kml Openlayers View """
    def get_data(self):
        return self.context.getFile().data


class KmlOpenLayersView(BrowserView):
    """ Kml Openlayers View """

    implements(IMultiLayersView)

    xsd = 'ogckml22.xsd'
    template = ViewPageTemplateFile('kmlopenlayersview.pt')

    def validate(self, xml):
        full_path = os.path.realpath(__file__)
        path, file = os.path.split(full_path)
        xsd_source = os.sep.join([path, self.xsd])

        f = open(xsd_source)
        xmlschema_doc = etree.parse(f, base_url=path + '/' + self.xsd)
        f.close()
        xmlschema = etree.XMLSchema(xmlschema_doc)
        parser = etree.XMLParser(schema=xmlschema)
        try:
            etree.fromstring(xml.data, parser)
            return True
        except etree.XMLSyntaxError, err:
            return str(err)
        return

    def __call__(self):
        atfiles = self.context.listFolderContents({'portal_type': 'File'})
        validfiles = []
        errors = []
        for atfile in atfiles:
            check = self.validate(atfile.getFile())
            if check is True:
                validfiles.append(atfile)
            else:
                errors.append({'error': check, 'title': atfile.Title()})
        self.request.set('validfiles', validfiles)
        self.request.set('errors', errors)
        return self.template()


class KMLMapLayer(MapLayer):
    """map layer see: collective.geo.mapwidget
    """
    @memoizedproperty
    def jsfactory(self):
        title = self.context.Title().replace("'", "\'")
        template = self.context.restrictedTraverse('kml-searchlayers')()
        return template % (title, self.context.absolute_url())


class KMLMapLayers(MapLayers):
    '''create all layers for this view.
    '''
    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        for item in self.context.listFolderContents({'portal_type': 'File'}):
            layers.append(KMLMapLayer(context=item.getObject()))
        return layers
